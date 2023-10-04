from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import Material


class MaterialSerializer(serializers.ModelSerializer):
    """
    Serializer for the Material model with Base64-encoded image support.

    This serializer extends the ModelSerializer provided by Django REST framework.
    It includes the Base64ImageField to handle image uploads as Base64-encoded strings.
    
    Attributes:
        image (Base64ImageField): Field for handling Base64-encoded image data.
    
    Meta:
        model (Material): The Material model class.
        fields (tuple): A tuple containing the names of fields to be included
            in the serialized output. '__all__' includes all fields from the model.
    """

    image = Base64ImageField()

    class Meta:
        model = Material
        fields = '__all__'

