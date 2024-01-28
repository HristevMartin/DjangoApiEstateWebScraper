from django.db.models import F
from django.db.models import FloatField
from django.db.models.expressions import Func
from django.db.models.functions import Cast, Coalesce
from rest_framework import generics, status
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from UK_Estate_app.models import Sample, Inquiry3
from UK_Estate_app.serializers import (
    SampleSerializer,
    PropertySerializer,
    PropertyDetailSerializer,
    InquirySerializer,
)
from .models import Property
from .pagination import StandardResultsSetPagination


class SampleApiView(ListCreateAPIView):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    # permission_classes = [IsAuthenticated]


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


class PropertyApiViewPagination(ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        sort_by = self.request.query_params.get("sort", "id")
        area_filter = self.request.query_params.get("area", None)
        sort_area = self.request.query_params.get("sortArea", None)

        queryset = Property.objects.annotate(
            price_as_float=Cast(Replace("price_per_week"), FloatField())
        )

        # queryset = Property.objects.annotate(
        #     cleaned_price_per_week=Cast(Replace("price_per_week"), FloatField()),
        #     cleaned_price=Cast(
        #         Replace("price"),
        #         FloatField()
        #     ),
        #     price_as_float = Coalesce('cleaned_price_per_week', 'cleaned_price')
        # )

        # Filter by area
        if area_filter:
            queryset = queryset.filter(address__icontains=area_filter)

        if sort_area:
            queryset = queryset.filter(address__icontains=sort_area)

        # Sorting
        if "-" in sort_by:
            sort_order = F("price_as_float").desc(nulls_last=True)
        else:
            sort_order = F("price_as_float").asc(nulls_last=True)

        queryset = queryset.order_by(sort_order)

        return queryset


class ItemDetailView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializer

#     overwrite the get method to see the results send to the client
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        print(response.data)
        return response


from rest_framework.filters import OrderingFilter


class SortAreas(ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["area", "other_fields"]


class UniqueAreas(APIView):
    def get(self, request, format=None):
        unique_areas = Property.objects.values_list("address", flat=True).distinct()
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


from google.cloud import dialogflow_v2 as dialogflow
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response


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
