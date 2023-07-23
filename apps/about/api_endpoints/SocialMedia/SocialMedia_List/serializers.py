from rest_framework import serializers

from apps.about.models import SocialMedia


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ['social_media', 'link']
