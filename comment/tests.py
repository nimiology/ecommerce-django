from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from category.models import Category
from category.tests import get_user_token
from comment.models import Comment
from product.models import Product


class CommentAPITest(APITestCase):
    def setUp(self):
        self.user, self.token = get_user_token('Jane')
        self.category = Category.objects.create(name='test')
        self.product = Product.objects.create(name='test', description='test', category=self.category)
        self.comment = Comment.objects.create(owner=self.user, product=self.product,
                                              text='test')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_post_comment(self):
        response = self.client.post(reverse('comment:comment_list'),
                                    data={'product': self.product.pk, 'text': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_comment_not_authenticated(self):
        self.client.credentials()
        response = self.client.post(reverse('comment:comment_list'),
                                    data={'product': self.product.pk, 'text': 'test'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_comments_list(self):
        self.client.credentials()
        response = self.client.get(reverse('comment:comment_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_comment(self):
        self.client.credentials()
        response = self.client.get(
            reverse('comment:comment', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_comment_not_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=get_user_token('John')[1])
        response = self.client.delete(
            reverse('comment:comment', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment(self):
        response = self.client.delete(
            reverse('comment:comment', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_comment_like(self):
        response = self.client.post(reverse('comment:comment_like', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['likes'][0]['username'], 'Jane')
        response = self.client.post(reverse('comment:comment_like', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['likes']), 0)