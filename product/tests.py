from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from category.models import Category
from category.tests import get_user_token
from product.models import Product, Order


class ProductAPITest(APITestCase):
    def setUp(self):
        self.user, self.token = get_user_token('Jane', admin=True)
        self.category = Category.objects.create(name='test1')
        self.product = Product.objects.create(category=self.category, name='test', description='test')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_post_product(self):
        response = self.client.post(reverse(f'product:product_list'),
                                    data={'name': 'test2', 'category': self.category.pk, 'description': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_product_not_admin(self):
        user, token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.post(reverse(f'product:product_list'), data={'name': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_products_list(self):
        self.client.credentials()
        response = self.client.get(reverse(f'product:product_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product(self):
        self.client.credentials()
        response = self.client.get(
            reverse(f'product:product', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_product(self):
        response = self.client.put(
            reverse(f'product:product', kwargs={'pk': self.product.pk}),
            data={'name': 'test3', 'category': self.category.pk, 'description': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test3')

    def test_patch_product(self):
        response = self.client.patch(
            reverse(f'product:product', kwargs={'pk': self.product.pk}),
            data={'name': 'test3'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test3')

    def test_put_product_not_admin(self):
        user, token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.put(
            reverse(f'product:product', kwargs={'pk': self.product.pk}),
            data={'name': 'test3'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_product_not_admin(self):
        user, token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.patch(
            reverse(f'product:product', kwargs={'pk': self.product.pk}),
            data={'name': 'test3'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product(self):
        response = self.client.delete(
            reverse(f'product:product', kwargs={'pk': self.product.pk}), )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_product_not_admin(self):
        user, token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(
            reverse(f'product:product', kwargs={'pk': self.product.pk}), )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OrderAPITest(APITestCase):
    def setUp(self):
        self.user, self.token = get_user_token('Jane')
        self.category = Category.objects.create(name='test1')
        self.product = Product.objects.create(category=self.category, name='test', description='test')
        self.order = Order.objects.create(product=self.product, owner=self.user, address='test')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_post_order(self):
        response = self.client.post(reverse(f'product:order_list'),
                                    data={'product': self.product.pk, 'address': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_order_not_authenticated(self):
        self.client.credentials()
        response = self.client.post(reverse(f'product:order_list'), data={'address': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_orders_list(self):
        self.client.credentials()
        response = self.client.get(reverse(f'product:order_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_order(self):
        response = self.client.get(
            reverse(f'product:order', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_order(self):
        response = self.client.patch(
            reverse(f'product:order', kwargs={'pk': self.order.pk}),
            data={'address': 'test3'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['address'], 'test3')

    def test_put_order_not_owner(self):
        user, token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.put(
            reverse(f'product:order', kwargs={'pk': self.order.pk}),
            data={'name': 'test3'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_order_not_owner(self):
        user, token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.patch(
            reverse(f'product:order', kwargs={'pk': self.order.pk}),
            data={'name': 'test3'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)