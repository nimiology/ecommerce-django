from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from category.models import Category
from category.tests import get_user_token
from product.models import Product


class CategoryAPITest(APITestCase):
    def setUp(self):
        self.user, self.token = get_user_token('Jane', admin=True)
        self.category = Category.objects.create(name='test1')
        self.product = Product.objects.create(category=self.category, name='test', description='test')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_post_category(self):
        response = self.client.post(reverse(f'product:product_list'),
                                    data={'name': 'test2', 'category': self.category.pk, 'description': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_category_not_admin(self):
        user, token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.post(reverse(f'product:product_list'), data={'name': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_categories_list(self):
        self.client.credentials()
        response = self.client.get(reverse(f'product:product_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category(self):
        self.client.credentials()
        response = self.client.get(
            reverse(f'product:product', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_category(self):
        response = self.client.put(
            reverse(f'product:product', kwargs={'pk': self.category.pk}),
            data={'name': 'test3', 'category': self.category.pk, 'description': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test3')

    def test_patch_category(self):
        response = self.client.patch(
            reverse(f'product:product', kwargs={'pk': self.category.pk}),
            data={'name': 'test3'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test3')

    def test_put_category_not_admin(self):
        user, token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.put(
            reverse(f'product:product', kwargs={'pk': self.category.pk}),
            data={'name': 'test3'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_category_not_admin(self):
        user, token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.patch(
            reverse(f'product:product', kwargs={'pk': self.category.pk}),
            data={'name': 'test3'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category(self):
        response = self.client.delete(
            reverse(f'product:product', kwargs={'pk': self.category.pk}), )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_category_not_admin(self):
        user, token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(
            reverse(f'product:product', kwargs={'pk': self.category.pk}), )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
