from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase

from category.models import Category
from category import urls


def get_user_token(username, admin=False):
    user = get_user_model().objects.create(username=username, password='1234', is_staff=admin)
    refresh = RefreshToken.for_user(user)
    return user, f'Bearer {refresh.access_token}'


class CategoryTest(APITestCase):
    def setUp(self):
        self.user, self.token = get_user_token('Jane', admin=True)
        self.category = Category.objects.create(name='test1')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_post_category(self):
        response = self.client.post(reverse(f'{urls.app_name}:{urls.urlpatterns[0].name}'), data={'name': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_category_not_admin(self):
        user, token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.post(reverse(f'{urls.app_name}:{urls.urlpatterns[0].name}'), data={'name': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_categories_list(self):
        self.client.credentials()
        response = self.client.get(reverse(f'{urls.app_name}:{urls.urlpatterns[0].name}'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category(self):
        self.client.credentials()
        response = self.client.get(
            reverse(f'{urls.app_name}:{urls.urlpatterns[1].name}', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_category(self):
        response = self.client.put(
            reverse(f'{urls.app_name}:{urls.urlpatterns[1].name}', kwargs={'pk': self.category.pk}),
            data={'name': 'test3'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test3')

    def test_patch_category(self):
        response = self.client.patch(
            reverse(f'{urls.app_name}:{urls.urlpatterns[1].name}', kwargs={'pk': self.category.pk}),
            data={'name': 'test3'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test3')

    def test_put_category_not_admin(self):
        user, token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.put(
            reverse(f'{urls.app_name}:{urls.urlpatterns[1].name}', kwargs={'pk': self.category.pk}),
            data={'name': 'test3'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_category_not_admin(self):
        user, token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.patch(
            reverse(f'{urls.app_name}:{urls.urlpatterns[1].name}', kwargs={'pk': self.category.pk}),
            data={'name': 'test3'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_delete_category(self):
        response = self.client.delete(
            reverse(f'{urls.app_name}:{urls.urlpatterns[1].name}', kwargs={'pk': self.category.pk}), )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_category_not_admin(self):
        user, token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(
            reverse(f'{urls.app_name}:{urls.urlpatterns[1].name}', kwargs={'pk': self.category.pk}), )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
