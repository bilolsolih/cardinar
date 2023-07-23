from rest_framework import serializers

from apps.store.models.product import Product


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'collection', 'photo', 'price', 'status']
