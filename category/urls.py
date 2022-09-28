from django.urls import path

from category.views import CategoryListCreateAPI, CategoryRetrieveUpdateDestroyAPIView

app_name = 'category'

urlpatterns = [
    path('', CategoryListCreateAPI.as_view(), name='category_list'),
    path('<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category'),
]
