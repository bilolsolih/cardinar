from django.apps import apps
from rest_framework import serializers


class CartItemCreateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
    product_id = serializers.CharField()
    content_type = serializers.CharField()

    def validate(self, data):
        app_label, model_name = data.validated_data['content_type'].split('.')
        model = apps.get_model(app_label=app_label, model_name=model_name)
        product = model.objects.filter(pk=data.validated_data['product_id']).first()

        if product:
            validated_data = dict()
            validated_data['content_type'] = data['content_type']
            validated_data['product_id'] = data['product_id']
            validated_data['quantity'] = data['quantity']
            validated_data['title'] = product.title
            validated_data['price'] = product.price
            validated_data['url'] = product.photo.url
            return validated_data
        else:
            raise serializers.ValidationError('Such product doesn\'t exist.')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
