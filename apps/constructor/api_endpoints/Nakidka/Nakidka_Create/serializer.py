from rest_framework import serializers

from apps.store.models.product import Nakidka


class NakidkaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nakidka
        fields = ['id', 'category', 'title', 'type', 'status', 'photo', 'price', 'building_material', 'created']
