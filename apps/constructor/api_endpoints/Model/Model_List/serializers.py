from rest_framework.serializers import ModelSerializer

from apps.constructor.models import CustomProductModel


class CustomProductModelListSerializer(ModelSerializer):
    class Meta:
        model = CustomProductModel
        fields = ['id', 'category', 'title', 'photo']
