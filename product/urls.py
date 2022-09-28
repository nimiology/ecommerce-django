from django.urls import path

from product.views import ProductRetrieveUpdateDestroyAPIView, ProductListCreateAPI, OrderListCreateAPIView, \
    OrderRetrieveUpdateAPIView

app_name = 'product'

urlpatterns = [
    path('product/', ProductListCreateAPI.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product'),

    path('order/', OrderListCreateAPIView.as_view(), name='order_list'),
    path('order/<int:pk>/', OrderRetrieveUpdateAPIView.as_view(), name='order'),
]
