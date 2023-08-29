from rest_framework import serializers


class CreateUserCardSerializer(serializers.Serializer):
    card_number = serializers.CharField()
    expire_date = serializers.CharField()
