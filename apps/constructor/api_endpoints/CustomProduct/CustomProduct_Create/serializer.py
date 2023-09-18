from rest_framework import serializers

from apps.constructor.models import CustomProduct


class CustomProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomProduct
        fields = ['category', 'product', 'product_model', 'full_name', 'phone_number', 'email', 'photo', 'remove_logo', 'remove_podpyatnik']
