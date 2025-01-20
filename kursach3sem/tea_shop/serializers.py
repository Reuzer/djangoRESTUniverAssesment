"""Serializers for TeaCategory and TeaProduct models."""

from rest_framework import serializers
from .models import TeaCategory, TeaProduct


class TeaCategorySerializer(serializers.ModelSerializer):
    """Serializer for the TeaCategory model."""

    class Meta:
        """Meta class specifying the model and fields to serialize."""
        model = TeaCategory
        fields = '__all__'


class TeaProductSerializer(serializers.ModelSerializer):
    """Serializer for the TeaProduct model."""

    class Meta:
        """Meta class specifying the model and fields to serialize."""
        model = TeaProduct
        fields = '__all__'
