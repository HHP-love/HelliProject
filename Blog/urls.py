from django.urls import path, include
from .views import PostCreateView, FileUploadView, PostListView, PostRetrieveUpdateDestroyAPIView
from .views import documentation_view


urlpatterns = [
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/file_upload/', FileUploadView.as_view(), name='file-upload'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),
    path('documentation/', documentation_view, name='documentation'),
]




