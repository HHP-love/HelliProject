from django.urls import path, include
from .views import PostCreateView, FileUploadView, PostListView, PostRetrieveUpdateDestroyAPIView, CommentListCreateView, CommentUpdateDeleteView
from .views import documentation_view
from django.urls import path
from .views import CommentListCreateView, CommentUpdateDeleteView

urlpatterns = [
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/file_upload/', FileUploadView.as_view(), name='file-upload'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),
    path('documentation/', documentation_view, name='documentation'),
    path("comments/", CommentListCreateView.as_view(), name="comment-list-create"),
    path("comments/<int:pk>/", CommentUpdateDeleteView.as_view(), name="comment-detail"),
]







