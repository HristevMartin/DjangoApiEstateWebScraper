from datetime import datetime
from tokenize import TokenError

import jwt
from django.contrib.auth.models import User
from auth_app.models import CustomUser

from django.utils import timezone
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken

from auth_app.models import BlacklistedToken
from auth_app.serializers import (
    UserSerializer,
)  # You should create a serializer for user registration data


@api_view(["POST"])
def register_user(request):
    print("request data", request.data)

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        # Create a new user
        serializer.save()

        # Generate tokens for the newly registered user
        # refresh = RefreshToken.for_user(user)
        # return Response({
        #     'access_token': str(refresh.access_token),
        #     'refresh_token': str(refresh)
        # }, status=status.HTTP_201_CREATED)

        # Return tokens in the response
        return Response("successfully registered", status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)

        except TokenError as e:
            raise InvalidToken(e.args[0])

        except Exception as e:
            print("error", e)
            return Response(
                {"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST
            )
            # raise InvalidToken(e.args[0])

        user = CustomUser.objects.get(email=request.data["email"])

        return Response(
            {
                "access_token": serializer.validated_data["access"],  # Access token
                "refresh_token": serializer.validated_data["refresh"],  # Refresh token
                "id": user.id,
                "email": user.email,
            }
        )


@api_view(["POST"])
def google_auth(request):
    google_token = request.data.get("google_token")

    try:
        # Validate the Google token and get user info
        idinfo = id_token.verify_oauth2_token(
            google_token,
            requests.Request(),
            "419141935816-l55gn89pm881kmsv0q82at4iga8a6fkh.apps.googleusercontent.com",
        )
        email = idinfo["email"]

        # Find or create user
        # user, created = User.objects.get_or_create(
        #     email=email, defaults={"username": email}
        # )

        user, created = CustomUser.objects.get_or_create(email=email)

        # Issue custom tokens
        refresh = RefreshToken.for_user(user)

        data_to_return = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "id": user.id,
            "email": user.email,
        }

        print("data_to_return", data_to_return)

        return Response(data_to_return, status=status.HTTP_200_OK)
    except Exception as ex:
        print('ex', ex)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = []  # This will override the default setting for this view only
    # permission_classes = []

    def delete(self, request):
        try:
            token = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
            decoded_token = jwt.decode(token, options={"verify_signature": False})
            print(request.user)
            expiration_date = timezone.make_aware(
                datetime.fromtimestamp(decoded_token["exp"])
            )
            if request.user.is_authenticated:
                BlacklistedToken.objects.create(
                    user=request.user, token=token, expires_at=expiration_date
                )

            print('show me the token', token)
            print('successfully logged out')
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            import logging
            logging.info('the reason for failing is', e)
            print('the reason for failing is', e)
            return Response(
                {"error": "Logout failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
