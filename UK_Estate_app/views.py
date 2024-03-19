import time

from django.conf import settings
from django.db.models import F
from django.db.models import FloatField
from django.db.models import Q
from django.db.models.expressions import Func
from django.db.models.functions import Cast
from django.http import JsonResponse
from elasticsearch import Elasticsearch
from google.cloud import dialogflow_v2 as dialogflow
from requests import head
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from UK_Estate_app.models import Inquiry3
from UK_Estate_app.permissions import IsNotDefaultGroupUser
from UK_Estate_app.serializers import (
    PropertySerializer,
    PropertyDetailSerializer,
    InquirySerializer,
)
from UK_Estate_app.utils import range_price_buckets
from .models import Property
from .pagination import StandardResultsSetPagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control

class PropertyApiView(ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Property.objects.all()[:20]


class Replace(Func):
    function = "REPLACE"
    template = "%(function)s(%(expressions)s, ',', '')"


def is_image_url_valid(url):
    response = head(url)
    return response.status_code == 200


es_client = Elasticsearch(settings.ELASTICSEARCH_URL)

@method_decorator(cache_control(max_age=20), name='dispatch')
class PropertyApiViewPagination(ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated, IsNotDefaultGroupUser]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        sort_by = self.request.query_params.get("sort", "id")
        area_filter = self.request.query_params.get("area", None)
        sort_area = self.request.query_params.get("sortArea", None)
        sort_country = self.request.query_params.get("country", None)
        price_range = self.request.query_params.get("price", None)
        print(price_range)

        queryset = Property.objects.annotate(
            price_as_float=Cast(Replace("price_per_week"), FloatField())
        )

        # Exclude properties with price_per_week less than 100
        queryset = queryset.exclude(price_as_float__lt=100)

        if area_filter:
            queryset = queryset.filter(address__icontains=area_filter)

        if sort_area:
            queryset = queryset.filter(address__icontains=sort_area)

        if sort_country and sort_country.lower() != 'all':
            queryset = queryset.filter(country__icontains=sort_country)

        # Filtering by price range
        if price_range:
            try:
                lower_bound, upper_bound = map(int, [x.strip().replace(" ", "") for x in price_range.split("-")])
                queryset = queryset.filter(price_as_float__gte=lower_bound, price_as_float__lte=upper_bound)
            except (ValueError, TypeError):
                raise ValidationError("Invalid price range format.")

        # Sorting
        if "-" in sort_by:
            sort_order = F("price_as_float").desc(nulls_last=True)
        else:
            sort_order = F("price_as_float").asc(nulls_last=True)
        if sort_country == 'all' or sort_country == 'BG':
            from django.db.models import Q

            queryset = queryset.exclude(Q(price_per_week='0') | Q(price_per_week='1') | Q(price_per_week='2'))
            queryset = queryset.order_by(sort_order)

        queryset = queryset.order_by(sort_order)

        return queryset


class ItemDetailView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializer

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        print(response.data)
        return response


class UniqueAreas(APIView):
    def get(self, request, format=None):
        # Get the country parameter from the query string
        country = request.query_params.get('country', None)
        search_area = request.query_params.get('searchArea', None)

        if country:
            properties = Property.objects.filter(country__iexact=country)
        else:
            properties = Property.objects.all()

        if search_area:
            properties = properties.filter(address__icontains=search_area)

        unique_areas = properties.values_list("address", flat=True).distinct()

        return Response(unique_areas)


class InquiryCreateView(generics.CreateAPIView):
    queryset = Inquiry3.objects.all()
    serializer_class = InquirySerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = InquirySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def dialogflow_request(request):
    # Initialize Dialogflow client
    project_id = 'my-demo-402415'

    session_id = str(request.data['user_id']) + 'random'

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    # Get the message from the POST request made by the frontend
    user_question = request.data['message']
    text_input = dialogflow.types.TextInput(text=user_question, language_code='en')
    query_input = dialogflow.types.QueryInput(text=text_input)

    try:
        # Send the text to Dialogflow's session client
        response = session_client.detect_intent(session=session, query_input=query_input)
        # Fetch the response from Dialogflow
        reply = response.query_result.fulfillment_text

        # Return the reply to the frontend
        return JsonResponse([
            {'reply': user_question, 'sender': 'user'},
            {'bot_reply': reply, 'sender': 'bot'}
        ],
            safe=False)

    except Exception as e:
        return Response(str(e), status=400)


class UniqueCountry(APIView):
    def get(self, request, format=None):

        searchArea = self.request.query_params.get('searchArea')

        if searchArea:
            unique_areas = Property.objects.filter(address__icontains=searchArea).values_list("country",
                                                                                              flat=True).distinct()
        else:
            unique_areas = Property.objects.values_list("country", flat=True).distinct()

        return Response(unique_areas)


class GetPriceRanges(APIView):
    def get(self, request):
        searchArea = self.request.query_params.get('searchArea')
        sortCountry = self.request.query_params.get('sortCountry')

        query = Q()

        if searchArea:
            query &= Q(address__icontains=searchArea)

        if sortCountry:
            query &= Q(country__icontains=sortCountry)

        properties_in_area = Property.objects.filter(query)

        price_ranges = properties_in_area.values_list("price_per_week", flat=True).distinct()

        filtered_price_ranges = [x for x in price_ranges if x not in [str(x) for x in range(0, 101)]]

        price_ranges = range_price_buckets(filtered_price_ranges)
        sorted_price_ranges = sorted(price_ranges, key=lambda x: int(x.split('-')[0].replace(' ', '')))

        return Response(sorted_price_ranges)
