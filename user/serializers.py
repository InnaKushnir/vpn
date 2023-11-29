from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "is_staff", "email", "password")
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "is_staff", "email", "password", "first_name", "last_name")
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)

        user = get_user_model().objects.create_user(**validated_data)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()
        return user

