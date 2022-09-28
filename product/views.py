from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from category.permissions import ReadOnly
from comment.permissions import IsOwner
from product.models import Product, Order
from product.serializers import ProductSerializer, OrderSerializer


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


class OrderListCreateAPIView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = {'owner': ['exact'],
                        'product': ['exact'],
                        'address': ['contains', 'exact'],
                        'created_date': ['exact', 'gte', 'lte'],
                        'delivery_date': ['exact', 'gte', 'lte']
                        }
    ordering_fields = ['owner', 'product', 'address', 'created_date', 'delivery_date']

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        return super(OrderListCreateAPIView, self).post(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class OrderRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOwner]

    def perform_update(self, serializer):
        instance = self.get_object()
        return serializer.save(owner=instance.owner, product=instance.product)