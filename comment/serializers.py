from rest_framework.serializers import ModelSerializer
from djoser.serializers import UserSerializer

from comment.models import Comment
from product.serializers import ProductSerializer


class CommentSerializer(ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['product'] = ProductSerializer()
        self.fields['likes'] = UserSerializer(many=True)
        return super(CommentSerializer, self).to_representation(instance)