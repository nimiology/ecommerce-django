from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, SAFE_METHODS

from category.models import Category
from category.permissions import ReadOnly
from category.serializers import CategorySerializer


class CategoryListCreateAPI(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = {'parent': ['exact'],
                        'name': ['contains', 'exact'],
                        }
    ordering_fields = ['parent', 'name']

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        return super(CategoryListCreateAPI, self).post(request, *args, **kwargs)


class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser | ReadOnly]
