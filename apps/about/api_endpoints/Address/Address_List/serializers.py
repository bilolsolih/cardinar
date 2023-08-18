from rest_framework import serializers
from apps.about.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['region', 'district', 'street', 'house_no']
