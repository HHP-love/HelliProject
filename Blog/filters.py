import django_filters
from django.db.models import Q
from .models import Post, Comment

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")  # جستجو در عنوان پست
    category = django_filters.CharFilter(lookup_expr="iexact")  # فیلتر بر اساس دسته‌بندی
    is_published = django_filters.BooleanFilter()  # فیلتر بر اساس انتشار
    publish_at = django_filters.DateTimeFromToRangeFilter()  # فیلتر بر اساس بازه زمانی انتشار
    created_at = django_filters.DateTimeFromToRangeFilter()  # فیلتر بر اساس بازه زمانی ایجاد پست

    class Meta:
        model = Post
        fields = ['title', 'category', 'is_published', 'publish_at', 'created_at']




from django.contrib.auth import get_user_model

User = get_user_model()

class CommentFilter(django_filters.FilterSet):
    post = django_filters.NumberFilter(field_name="post__id")  
    national_code = django_filters.CharFilter(method="filter_by_national_code")  

    class Meta:
        model = Comment
        fields = ["post", "national_code"]

    def filter_by_national_code(self, queryset, name, value):
        return queryset.filter(user__national_code=value)  
