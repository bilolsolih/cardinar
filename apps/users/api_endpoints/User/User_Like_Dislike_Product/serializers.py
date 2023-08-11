from django.apps import apps
from rest_framework import serializers


class UserLikeDislikeSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    content_type = serializers.CharField()

    def validate(self, data):
        app_label, model_name = data.validated_data['content_type'].split('.')
        model = apps.get_model(app_label=app_label, model_name=model_name)
        product = model.objects.filter(pk=data.validated_data['product_id'], is_constructed=False).first()

        if product:
            return data
        else:
            raise serializers.ValidationError('Such products doesn\'t exist.')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
