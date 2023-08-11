from rest_framework import serializers

from apps.store.models.product import Polik


class PolikCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polik
        fields = ['id', 'category', 'title', 'type', 'status', 'photo', 'price', 'building_material', 'created']
