from rest_framework import serializers

from apps.cart.models import CartItem
from apps.store.models.product import Product, Articul
from apps.store.models.product_parameters import CarModel


class CarModelInArticul(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = '__all__'


class ArticulInCartItem(serializers.ModelSerializer):
    car_model = CarModelInArticul(many=False)

    class Meta:
        model = Articul
        fields = '__all__'


class ProductInCartItem(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'photo', 'category_title']


class CartItemListSerializer(serializers.ModelSerializer):
    articul = ArticulInCartItem(many=False)
    product = ProductInCartItem(many=False)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'articul', 'quantity', 'cost']
