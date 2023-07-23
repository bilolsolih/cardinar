from rest_framework.generics import ListAPIView

from apps.store.models.product import Category
from .serializers import CategoryListSerializer


class CategoryListAPIView(ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()


__all__ = ['CategoryListAPIView']
