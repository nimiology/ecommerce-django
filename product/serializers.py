from rest_framework.serializers import ModelSerializer

from category.serializers import CategorySerializer
from product.models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['category'] = CategorySerializer()
        return super(ProductSerializer, self).to_representation(instance)