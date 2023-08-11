from django.apps import apps
from rest_framework import serializers

from apps.inquiries.models import Inquiry


class InquiryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ['full_name', 'phone_number', 'content_type', 'object_id', 'email']

    def validate(self, attrs):
        app_label, model_name = attrs['content_type'].split('.')
        product_model = apps.get_model(app_label=app_label, model_name=model_name)
        product = product_model.object.filter(pk=attrs['object_id'])
        if not product:
            raise serializers.ValidationError('Such product doesn\'t exist.')
        return attrs
