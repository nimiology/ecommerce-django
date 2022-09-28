from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAdminUser

from category.permissions import ReadOnly
from picture.models import ProductPicture
from picture.serializers import ProductPictureSerializer


class ProductPictureListCreateAPI(ListCreateAPIView):
    queryset = ProductPicture.objects.all()
    serializer_class = ProductPictureSerializer
    filterset_fields = {'product': ['exact'],
                        }
    ordering_fields = ['product', '?']

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        return super(ProductPictureListCreateAPI, self).post(request, *args, **kwargs)


class CategoryRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    queryset = ProductPicture.objects.all()
    serializer_class = ProductPictureSerializer
    permission_classes = [IsAdminUser | ReadOnly]
