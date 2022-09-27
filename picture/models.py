from django.db import models

from product.models import Product
from users.utils import upload_file


class ProductPicture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pictures')
    picture = models.ImageField(upload_to=upload_file)

    def __str__(self):
        return self.product.name
