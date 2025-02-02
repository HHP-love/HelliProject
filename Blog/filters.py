import django_filters
from django.db.models import Q
from .models import Post

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")  # جستجو در عنوان پست
    category = django_filters.CharFilter(lookup_expr="iexact")  # فیلتر بر اساس دسته‌بندی
    is_published = django_filters.BooleanFilter()  # فیلتر بر اساس انتشار
    publish_at = django_filters.DateTimeFromToRangeFilter()  # فیلتر بر اساس بازه زمانی انتشار
    created_at = django_filters.DateTimeFromToRangeFilter()  # فیلتر بر اساس بازه زمانی ایجاد پست

    class Meta:
        model = Post
        fields = ['title', 'category', 'is_published', 'publish_at', 'created_at']
