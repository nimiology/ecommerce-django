from django.urls import path

from picture.views import ProductPictureListCreateAPI, CategoryRetrieveDestroyAPIView

app_name = 'picture'

urlpatterns = [
    path('', ProductPictureListCreateAPI.as_view(), name='product_picture_list'),
    path('<int:pk>/', CategoryRetrieveDestroyAPIView.as_view(), name='product_picture'),
]