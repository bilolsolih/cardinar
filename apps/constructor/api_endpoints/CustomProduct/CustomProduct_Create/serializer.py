from rest_framework import serializers

from apps.constructor.models import CustomProduct


class CustomProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomProduct
        fields = ['category', 'product_model', 'central_part', 'back_part', 'rear_part', 'stitch', 'kant', 'remove_logo', 'remove_podpyatnik']

    def validate(self, attrs):
        category = attrs['category']
        pm = getattr(attrs, 'product_model', None)
        if not pm:
            raise serializers.ValidationError({'product_model': 'model must be specified'})
        cp = getattr(attrs, 'central_part', None)
        bp = getattr(attrs, 'back_part', None)
        rp = getattr(attrs, 'rear_part', None)
        s = getattr(attrs, 'stitch', None)
        k = getattr(attrs, 'kant', None)
        match category:
            case 'c':
                if not cp or not bp or not rp or not s or not k:
                    raise serializers.ValidationError('Missing some fields')
            case 'n' | 'p':
                if not cp or not rp:
                    raise serializers.ValidationError('Missing some fields')
        return attrs
