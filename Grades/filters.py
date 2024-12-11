import django_filters

from .models import Semester

class SemesterFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name (contains)')
    start_date = django_filters.DateFilter(lookup_expr='gte', label='Start Date (from)')
    end_date = django_filters.DateFilter(lookup_expr='lte', label='End Date (to)')
    
    class Meta:
        model = Semester
        fields = ['name', 'start_date', 'end_date']



from .models import Subject

class SubjectFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name (contains)')
    code = django_filters.CharFilter(lookup_expr='exact', label='Code (exact match)')

    class Meta:
        model = Subject
        fields = ['name', 'code']
