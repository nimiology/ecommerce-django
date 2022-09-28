from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAdminUser

from category.permissions import ReadOnly
from product.models import Product
from product.serializers import ProductSerializer


class ProductListCreateAPI(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = {'category': ['exact'],
                        'name': ['contains', 'exact'],
                        'description': ['contains', 'exact'],
                        'price': ['exact', 'gte', 'lte'],
                        'count': ['exact', 'gte', 'lte']
                        }
    ordering_fields = ['category', 'name', 'description', 'price', 'count', ]

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        return super(ProductListCreateAPI, self).post(request, *args, **kwargs)


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser | ReadOnly]


