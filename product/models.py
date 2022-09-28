from django.contrib.auth import get_user_model
from django.db import models

from category.models import Category


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    address = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)

