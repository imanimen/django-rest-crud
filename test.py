from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.test import override_settings
from django.db import connection
from django.db.backends.utils import CursorWrapper
from myapp.models import Item
from myapp.serializers import ItemSerializer


class ItemViewTestCase(APITestCase):
    def setUp(self):
        self.item1 = Item.objects.create(name='item1', description='description1')
        self.item2 = Item.objects.create(name='item2', description='description2')

    def test_get_data(self):
        url = reverse('get-data')
        with connection.cursor() as cursor:
            cursor = CursorWrapper(cursor, connection)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['name'], self.item1.name)

    def test_add_data(self):
        url = reverse('add-data')
        data = {'name': 'item3', 'description': 'description3'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 3)

    def test_update_data(self):
        url = reverse('update-data', args=[self.item1.id])
        data = {'name': 'new-name', 'description': 'new-description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.name, 'new-name')
        self.assertEqual(self.item1.description, 'new-description')

    def test_delete_data(self):
        url = reverse('delete-data', args=[self.item1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 1)