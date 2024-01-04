from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("uk-estate-property/", include("UK_Estate_app.urls")),
    path("auth_app/", include("auth_app.urls")),
]
