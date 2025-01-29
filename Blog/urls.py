from django.urls import path, include
from .views import PostCreateView, FileUploadView, PostListView
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/file_upload/', FileUploadView.as_view(), name='file-upload'),
]




