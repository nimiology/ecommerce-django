from rest_framework.serializers import ModelSerializer

from picture.models import ProductPicture
from product.serializers import ProductSerializer


class ProductPictureSerializer(ModelSerializer):
    class Meta:
        model = ProductPicture
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['product'] = ProductSerializer(read_only=True)
        return super(ProductPictureSerializer, self).to_representation(instance)
