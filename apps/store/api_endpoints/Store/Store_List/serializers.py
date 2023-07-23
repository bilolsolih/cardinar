from rest_framework.serializers import ModelSerializer

from apps.store.models.store import Store


class StoreListSerializer(ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'title', 'phone_number', 'region', 'district', 'address', 'orient']
