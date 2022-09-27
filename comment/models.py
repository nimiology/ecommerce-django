from django.contrib.auth import get_user_model
from django.db import models

from product.models import Product
from users.models import MyUser


class Comment(models.Model):
    owner = models.ForeignKey (get_user_model(), on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='childrens')
    created_date = models.DateTimeField(auto_now_add=True)
    upvote = models.ManyToManyField(MyUser, blank=True, related_name='comment_upvotes')
    downvote = models.ManyToManyField(MyUser, blank=True, related_name='comment_downvotes')
