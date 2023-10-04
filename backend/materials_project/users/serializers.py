from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.validators import UniqueValidator
from .models import User


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Custom serializer for user registration with additional validations.
    """

    # Email field with unique validation
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    # Username field with unique validation
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'email', 'id', 'password', 'username', 'first_name', 'last_name')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


class CustomUserSerializer(UserSerializer):
    """
    Custom serializer for user details.
    """
    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name')
