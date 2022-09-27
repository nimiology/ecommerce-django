from django.db import models


class Category(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='category')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
