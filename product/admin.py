from django.contrib import admin

from product.models import Product, Order

admin.site.register(Product)
admin.site.register(Order)