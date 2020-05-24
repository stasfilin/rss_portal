from django.contrib.auth.models import User
from rest_framework import serializers


class UserBaseSerializer(serializers.ModelSerializer):
    """
    User Base Serializer
    Password mark like write_only.
    """

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}


class SignUpSerializer(UserBaseSerializer):
    """
    Signup Serializer for creating new user
    """

    def create(self, validated_data) -> User:
        """
        Function for creating new user, set password
        :param validated_data: Validated data from Serializer
        :return: User Object
        """
        user = User(email=validated_data["email"], username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user
