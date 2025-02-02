from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PostFilter
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema
from .models import Post
from .serializers import PostSerializer
import os

class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Create a new blog post",
        description="""
        This endpoint allows authenticated users to create a new blog post.

        **Validation Rules:**
        - `title`: Required, at least 5 characters.
        - `main_image`: Optional, must be an image.
        - `content`: Required, must be a valid JSON list.
        - `publish_at`: If set, must be in the future.

        **Response:**
        - `201 Created` on success.
        - `400 Bad Request` if validation fails.
        """,
        request=PostSerializer,
        responses={201: PostSerializer, 400: {"description": "Validation error"}},
    )
    def create(self, request, *args, **kwargs):
        """Create a new post"""
        return super().create(request, *args, **kwargs)





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        file_path = os.path.join("media", "uploads", file.name)
        try:
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        except Exception as e:
            return Response({"error": f"Failed to save the file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"file_url": f"/media/uploads/{file.name}"}, status=status.HTTP_201_CREATED)

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import Post
from .serializers import PostListSerializer

class PostPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'  # اگر بخواهید سایز صفحه را از URL بگیرید
    max_page_size = 100  # بیشترین تعداد آیتم‌ها در یک صفحه

# لیست پست‌ها
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter


# views.py

class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: دریافت جزئیات یک پست
    PUT/PATCH: ویرایش پست
    DELETE: حذف پست
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer





from django.shortcuts import render

def documentation_view(request):
    """
    این view صفحه مستندات API را رندر می‌کند.
    """
    return render(request, 'documentation.html')