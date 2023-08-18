from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.models import User


class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.api_client = APIClient()
        cls.defaults = {
            'username': 'testuser',
            'first_name': 'test',
            'last_name': 'abul test',
            'phone_number': '+998900000000',
            'email': 'test@test.com',
            'password1': 'password1234',
            'password2': 'password1234'
        }

    def test_basic_full(self):
        # registering a new user
        response = self.api_client.post(
            path=reverse('users:user_register'),
            format='json',
            data=self.defaults
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(User.objects.filter(username='testuser'))

        # logging in with the user created above
        response = self.api_client.post(
            path=reverse('users:user_login'),
            format='json',
            data={
                'username': 'testuser',
                'password': 'password1234'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # already logged in but trying to register a new user
        user = User.objects.get(username='testuser')
        self.api_client.force_login(user)
        response = self.api_client.post(
            path=reverse('users:user_register'),
            format='json',
            data={
                'username': 'testuser1',
                'first_name': 'test2',
                'last_name': 'abul test2',
                'phone_number': '+998900000001',
                'email': 'test2@test.com',
                'password1': 'password12345',
                'password2': 'password12345'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # already logged in but trying to log in again.
        response = self.api_client.post(
            path=reverse('users:user_login'),
            format='json',
            data={
                'username': 'testuser',
                'password': 'password1234'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # updating the user
        response = self.api_client.patch(
            path=reverse('users:user_update'),
            format='json',
            data={
                'first_name': 'Bilol',
                'last_name': 'Solih',
                'email': 'Bilol@gmail.com',
                'phone_number': '+998912958899'
            }
        )
        user = User.objects.get(username='testuser')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(getattr(user, 'first_name', None), 'Bilol')
        self.assertEqual(getattr(user, 'last_name', None), 'Solih')
        self.assertEqual(getattr(user, 'email', None), 'Bilol@gmail.com')
        self.assertEqual(getattr(user, 'phone_number', None), '+998912958899')

        # logging out
        response = self.api_client.get(path=reverse('users:user_logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # trying to update again without loggin in
        response = self.api_client.patch(
            path=reverse('users:user_update'),
            format='json',
            data={
                'first_name': 'Bilolbek',
                'last_name': 'Solihjon',
                'email': 'Bilolbek@gmail.com',
                'phone_number': '+998912968899'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
