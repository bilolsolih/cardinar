from rest_framework import serializers

from apps.about.models import Email


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['email']
