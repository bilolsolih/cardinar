from rest_framework import serializers

from apps.store.models.product import CarCover


class CarCoverCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCover
        fields = ['id', 'category', 'title', 'photo', 'price', 'status', 'building_material', 'created']
