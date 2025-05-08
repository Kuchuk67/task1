from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "password",
            "email",
            "nick_telegram",
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "nick_telegram"]

    def create(self, validated_data):
        validated_data["password"] = make_password(
            validated_data.get("password"))
        return super(UserCreateSerializer, self).create(validated_data)
