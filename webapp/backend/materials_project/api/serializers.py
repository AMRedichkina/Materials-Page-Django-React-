from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import Material


class MaterialSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Material
        fields = '__all__'

