from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from auth_app.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=False, allow_blank=True)
    # username = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email","username", "password"]
        # extra_kwargs = {'password': {'write_only': True}}

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)

        self.fields["password2"] = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        validated_data.pop("password2", None)

        username = validated_data.get("username") or None
        user = CustomUser(email=validated_data["email"], username=username)
        try:
            user.set_password(validated_data["password"])
            user.save()
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # def validate(self, attrs):
    #     data = super().validate(attrs)
    #     data["username"] = self.user.username
    #     return data

    def validate(self, attrs):
        attrs[self.username_field] = attrs.get(self.username_field)
        return super().validate(attrs)