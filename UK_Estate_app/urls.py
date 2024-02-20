from django.urls import path

from UK_Estate_app.views import (
    PropertyApiView,
    PropertyApiViewPagination,
    ItemDetailView,
    UniqueAreas,
    InquiryCreateView, dialogflow_request, UniqueCountry, GetPriceRanges,
)

urlpatterns = (
    # path("sample/", SampleApiView.as_view(), name="sample"),
    path("property2/", PropertyApiView.as_view(), name="property"),
    path(
        "property-pagination/",
        PropertyApiViewPagination.as_view(),
        name="property-pagination",
    ),
    path("items/<int:pk>/", ItemDetailView.as_view(), name="item-detail"),
    path("unique-areas/", UniqueAreas.as_view(), name="unique-areas"),
    path("inquery_create/", InquiryCreateView.as_view(), name="inquery_view"),
    path("unique-country/", UniqueCountry.as_view(), name="inquery_view"),
    path('chatbot/', dialogflow_request, name='dialogflow_request'),
    path('price-range/', GetPriceRanges.as_view(), name='price-range'),
)
