from rest_framework import serializers

from apps.store.models.product import Product


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'category', 'title', 'photo', 'price', 'status', 'building_material', 'created']
