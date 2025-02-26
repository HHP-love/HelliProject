from django_filters import rest_framework as filters
from .models import Absence

class AbsenceFilter(filters.FilterSet):
    student__first_name = filters.CharFilter(lookup_expr='icontains')
    student__last_name = filters.CharFilter(lookup_expr='icontains')
    student__grade = filters.CharFilter()
    student__national_code = filters.CharFilter(lookup_expr='exact')
    date = filters.DateFilter()
    date_range = filters.DateFromToRangeFilter(field_name='date')
    status = filters.ChoiceFilter(choices=[('present', 'Present'), ('absent', 'Absent')])

    class Meta:
        model = Absence
        fields = [
            'student__first_name',
            'student__last_name',
            'student__grade',
            'student__national_code',
            'date',
            'date_range',
            'status',
        ]
