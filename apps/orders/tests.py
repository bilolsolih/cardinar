from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.users.models import User


class OrdersTestCase(TestCase):
    fixtures = [
        'fixtures/orders/payment_methods',
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
            'username': 'username',
            'first_name': 'first name',
            'last_name': 'last name',
            'phone_number': '+998901001010',
            'email': 'test@test.com'
        }
        user = User.objects.create(**defaults)
        user.set_password('password1234')
        self.api_client = APIClient()
        user.save()
        call_command('loaddata', 'fixtures/cart/carts')
        call_command('loaddata', 'fixtures/cart/cart_items')
        call_command('loaddata', 'fixtures/orders/orders')
        call_command('loaddata', 'fixtures/orders/order_items')
        self.api_client.force_login(user)

    def test_order_create(self):
        response = self.api_client.post(
            path=reverse('orders:order_create'),
            format='json',
            data={
                'pk': 29,
                'full_name': 'full name',
                'phone_number': '+998912968899',
                'email': 'nimadur@gmail.com',
                'delivery_type': 's',
                'payment_method': 1
            }

        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


