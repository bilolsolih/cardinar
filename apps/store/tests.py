from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


# Create your tests here.


class StoreTestCase(TestCase):
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
        'fixtures/store/products',
    ]

    @classmethod
    def setUpTestData(cls):
        cls.api_client = APIClient()

    def test_collections(self):
        response = self.api_client.get(reverse("store:collection_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

    def test_color(self):
        response = self.api_client.get(reverse("store:color_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

    def test_manufacturing(self):
        response = self.api_client.get(reverse("store:manufacturing_methods_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

    def test_picturetype(self):
        response = self.api_client.get(reverse("store:picture_type_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

    def test_size(self):
        response = self.api_client.get(reverse("store:size_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

    def test_style(self):
        response = self.api_client.get(reverse("store:style_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

    def test_targetroom(self):
        response = self.api_client.get(reverse("store:target_room_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

    def test_product(self):
        response = self.api_client.get(reverse('store:product_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

    def test_product_with_filters(self):
        filters = {
            'style': 1,
            'picture_type': 1,
            'color': 1
        }
        endpoint = reverse('store:product_list') + '?' + '&'.join([f'{key}={value}' for key, value in filters.items()])

        response = self.api_client.get(path=endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = list()
        for data in response.data:
            for key, value in filters.items():
                self.assertEqual(data[key], value)
        print('yorvordik')
