from rest_framework import serializers


class ApelsinPaySerializer(serializers.Serializer):
    transaction_id = serializers.CharField(required=True)
    cabinetId = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(required=True)
