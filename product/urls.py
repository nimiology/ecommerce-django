from django.urls import path

from product.views import ProductRetrieveUpdateDestroyAPIView, ProductListCreateAPI

app_name = 'product'

urlpatterns = [
    path('', ProductListCreateAPI.as_view(), name='product_list'),
    path('<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product'),
]
