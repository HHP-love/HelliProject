import django_filters
from .models import Grade

class GradeFilter(django_filters.FilterSet):
    student__first_name = django_filters.CharFilter(field_name='student__first_name', lookup_expr='exact')
    student__last_name = django_filters.CharFilter(field_name='student__last_name', lookup_expr='exact')
    category__name = django_filters.CharFilter(field_name='category__name', lookup_expr='exact')

    class Meta:
        model = Grade
        fields = ['student__first_name', 'student__last_name', 'category__name']
