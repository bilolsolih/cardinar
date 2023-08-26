from rest_framework.serializers import ModelSerializer

from apps.constructor.models import Part


class PartListSerializer(ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'
