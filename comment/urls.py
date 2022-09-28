from django.urls import path

from comment.views import CommentListCreateAPI, CommentRetrieveDestroyAPIView, CommentLikeAPI

app_name = 'comment'

urlpatterns = [
    path('', CommentListCreateAPI.as_view(), name='comment_list'),
    path('<int:pk>/', CommentRetrieveDestroyAPIView.as_view(), name='comment'),
    path('<int:pk>/like/', CommentLikeAPI.as_view(), name='comment_like')
]