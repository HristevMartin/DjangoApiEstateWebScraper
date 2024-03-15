from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import Group
from auth_app.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=False, allow_blank=True)
    # username = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        print('in the serilizer')
        fields = ["email", "username", "password"]
        # extra_kwargs = {'password': {'write_only': True}}

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)

        self.fields["password2"] = serializers.CharField(write_only=True)

    def validate(self, data):
        print('inside the validate')
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        print('creatinggg...')
        validated_data.pop("password2", None)

        username = validated_data.get("username") or None
        print('show me the username', username)
        user = CustomUser(email=validated_data["email"], username=username)

        # Assign the user to the default group

        try:
            user.set_password(validated_data["password"])
            user.save()
        except Exception as e:
            raise serializers.ValidationError(str(e))

        default_group, _ = Group.objects.get_or_create(name='Default')
        default_group.user_set.add(user)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs[self.username_field] = attrs.get(self.username_field)
        return super().validate(attrs)
