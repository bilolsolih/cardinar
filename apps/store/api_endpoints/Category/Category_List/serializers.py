from rest_framework.serializers import ModelSerializer

from apps.store.models.product import Category


class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']
