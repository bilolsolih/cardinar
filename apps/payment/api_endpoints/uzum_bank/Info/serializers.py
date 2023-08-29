from rest_framework import serializers


class ApelsinInfoSerializer(serializers.Serializer):
    cabinetId = serializers.IntegerField(required=True)
