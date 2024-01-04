from django.urls import path

from UK_Estate_app.views import (
    SampleApiView,
    PropertyApiView,
    PropertyApiViewPagination,
    ItemDetailView,
    SortAreas,
    UniqueAreas,
    InquiryCreateView,
)

urlpatterns = (
    path("sample/", SampleApiView.as_view(), name="sample"),
    path("property2/", PropertyApiView.as_view(), name="property"),
    path(
        "property-pagination/",
        PropertyApiViewPagination.as_view(),
        name="property-pagination",
    ),
    path("items/<int:pk>/", ItemDetailView.as_view(), name="item-detail"),
    path("sort-areas/", SortAreas.as_view(), name="unique-areas"),
    path("unique-areas/", UniqueAreas.as_view(), name="unique-areas"),
    path("inquery_create/", InquiryCreateView.as_view(), name="inquery_view"),
)
