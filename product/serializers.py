from djoser.serializers import UserSerializer
from rest_framework.serializers import ModelSerializer

from category.serializers import CategorySerializer
from product.models import Product, Order


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['category'] = CategorySerializer()
        return super(ProductSerializer, self).to_representation(instance)


class OrderSerializer(ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['product'] = ProductSerializer(read_only=True)
        return super(OrderSerializer, self).to_representation(instance)