from rest_framework import serializers

from apps.about.models import Banner


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'photo', 'text']
