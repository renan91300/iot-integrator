from djoser.serializers import (
    UserCreateSerializer as BaseUserRegistrationSerializer,
    UserCreatePasswordRetypeSerializer,
    UserSerializer,
)

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction

User = get_user_model()


class UserCreateSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        model = User
        fields = "__all__"


class UserCreatePasswordRetypeSerializer(UserCreatePasswordRetypeSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        model = User
        fields = ("id", "email", "name", "password", "is_staff")

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            user.is_active = True
            user.save(update_fields=["is_active"])
        return user


class UserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            "id",
            "name",
            "email",
            "is_staff",
            "is_active",
            "created_at",
            "updated_at",
            "last_login",
        )

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class UserDeleteSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ()
