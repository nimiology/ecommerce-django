from rest_framework.generics import ListCreateAPIView, GenericAPIView, RetrieveDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from comment.models import Comment
from comment.permissions import IsOwner
from comment.serializers import CommentSerializer


class CommentListCreateAPI(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filterset_fields = {'owner': ['exact'],
                        'product': ['exact'],
                        'parent': ['exact'],
                        'text': ['contains', 'exact'],
                        'created_date': ['exact', 'lte', 'gte'],
                        }
    ordering_fields = ['owner', 'product', 'parent', 'text', 'created_date']

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        return super(CommentListCreateAPI, self).post(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class CommentRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwner]

    def get(self, request, *args, **kwargs):
        self.permission_classes = []
        return super(CommentRetrieveDestroyAPIView, self).get(request, *args, **kwargs)


class CommentLikeAPI(GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        likes = instance.likes.all()
        if request.user in likes:
            instance.likes.remove(request.user)
        else:
            instance.likes.add(request.user)
        return Response(self.get_serializer(instance).data)

