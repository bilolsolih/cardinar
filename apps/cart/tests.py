from apps.users.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from time import sleep

from apps.cart.models import CartItem


class CartTestCase(TestCase):
    fixtures = [
        'fixtures/store/brands',
        'fixtures/store/collections',
        'fixtures/store/colors',
        'fixtures/store/manufacturingmethods',
        'fixtures/store/picturetypes',
        'fixtures/store/stores',
        'fixtures/store/styles',
        'fixtures/store/sizes',
        'fixtures/store/targetrooms',
        'fixtures/store/products'
    ]

    def setUp(self):
        defaults = {
            'username': 'testuser',
            'first_name': 'test',
            'last_name': 'abul test',
            'phone_number': '+998900000000',
            'email': 'test@test.com'
        }
        user = User.objects.create(**defaults)
        user.set_password('password1234')
        self.api_client = APIClient()
        user.save()
        call_command('loaddata', 'fixtures/cart/carts')
        call_command('loaddata', 'fixtures/cart/cart_items')
        self.cart = user.cart
        self.api_client.force_login(user)

    def test_cart_item_create(self):
        response = self.api_client.post(
            path=reverse('cart:cart_item_create'),
            format='json',
            data={
                'pk': 11,
                'cart': self.cart.pk,
                'product': '1',
                'quantity': '3',
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        item = CartItem.objects.filter(pk=11, cart=self.cart, product__pk=1, quantity=3)[0]
        self.assertIsNotNone(item)
        self.assertEqual(item.cost, item.product.price * item.quantity)

    def test_cart_item_list(self):
        response = self.api_client.get(
            path=reverse('cart:cart_item_list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = self.cart.items.all().values_list('id', flat=True)

        for data in response.data:
            self.assertIn(dict(data)['id'], items)

    def test_cart_item_update(self):
        for item in self.cart.items.all():
            response = self.api_client.patch(
                path=reverse('cart:cart_item_update', args=[item.pk]),
                format='json',
                data={
                    'quantity': 29
                }
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(self.cart.items.get(id=item.id).quantity, 29)

    def test_cart_item_delete(self):
        response = self.api_client.delete(
            path=reverse('cart:cart_item_delete', args=[7])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(CartItem.objects.filter(pk=7).first())
