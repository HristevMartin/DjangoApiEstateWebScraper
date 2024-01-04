from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from auth_app.views import (
    register_user,
    CustomTokenObtainPairView,
    google_auth,
    LogoutAPIView,
)

urlpatterns = (
    path(
        "token/obtain/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", register_user, name="register_user"),
    path("login/google/", google_auth, name="login_user"),
    path("logout/", LogoutAPIView.as_view(), name="logout_user"),
)
