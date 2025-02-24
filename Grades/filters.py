import django_filters

from .models import *

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



from .models import Classroom, Teacher, Student, Subject

class ClassroomFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Class Name')

    teachers = django_filters.ModelMultipleChoiceFilter(
        queryset=Teacher.objects.all(),
        field_name='teachers',
        to_field_name='id',
        label='Teachers'
    )

    students = django_filters.ModelMultipleChoiceFilter(
        queryset=Student.objects.all(),
        field_name='students',
        to_field_name='id',
        label='Students'
    )

    subject = django_filters.ModelChoiceFilter(
        queryset=Subject.objects.all(),
        field_name='subject',
        to_field_name='id',
        label='Subject'
    )

    start_time = django_filters.DateTimeFilter(field_name='start_time', lookup_expr='gte', label='Start Time (from)')
    end_time = django_filters.DateTimeFilter(field_name='end_time', lookup_expr='lte', label='End Time (to)')

    class Meta:
        model = Classroom
        fields = ['name', 'teachers', 'students', 'subject', 'start_time', 'end_time']


class GradeFilter(django_filters.FilterSet):
    classroom = django_filters.NumberFilter(field_name="classroom__id", lookup_expr='exact')
    category = django_filters.NumberFilter(field_name="category__id", lookup_expr='exact')
    student = django_filters.NumberFilter(field_name="student__id", lookup_expr='exact')

    class Meta:
        model = Grade
        fields = ['classroom', 'category', 'student']


class GradeCompareFilter(django_filters.FilterSet):
    student = django_filters.NumberFilter(field_name="student__id", lookup_expr='exact')

    class Meta:
        model = Grade
        fields = ['student']