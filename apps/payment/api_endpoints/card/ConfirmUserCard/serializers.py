from rest_framework import serializers


class ConfirmUserCardSerializer(serializers.Serializer):
    session = serializers.IntegerField()
    otp = serializers.CharField()
    card_number = serializers.CharField()
