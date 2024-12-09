from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from rest_framework import permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django_filters.rest_framework import DjangoFilterBackend
from Grades.models import *
from Grades.serializers import *
from Grades.filters import *  

class TeacherFilter(filters.FilterSet):
    classroom = filters.CharFilter(field_name="classes__name", lookup_expr="icontains")
    subject = filters.CharFilter(field_name="classes__subject__name", lookup_expr="icontains")

    class Meta:
        model = Teacher
        fields = ['classroom', 'subject']


@extend_schema(
    request=None,  # no request body
    responses=TeacherSerializer,
    parameters=[
        OpenApiParameter('classroom', description='Filter by classroom name (substring match)', required=False, type=str),
        OpenApiParameter('subject', description='Filter by subject name (substring match)', required=False, type=str),
    ],
    description="Retrieve teacher information with optional filters on classroom and subject."
)
class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Teacher.objects.prefetch_related('classes__subject').all()
    serializer_class = TeacherSerializer
    filter_backends = [filters.DjangoFilterBackend, SearchFilter]
    filterset_class = TeacherFilter
    search_fields = ['name']
    permission_classes = [permissions.IsAuthenticated]


class StudentFilter(filters.FilterSet):
    classroom = filters.CharFilter(field_name="classrooms__name", lookup_expr="icontains")
    grade = filters.CharFilter(field_name="grades__category__name", lookup_expr="icontains")

    class Meta:
        model = Student
        fields = ['classroom', 'grade']


@extend_schema(
    request=None,
    responses=StudentSerializer,
    parameters=[
        OpenApiParameter('classroom', description='Filter by classroom name (substring match)', required=False, type=str),
        OpenApiParameter('grade', description='Filter by grade category name (substring match)', required=False, type=str),
    ],
    description="Retrieve student information with optional filters on classroom and grade."
)
class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.prefetch_related('classrooms', 'grades__category').all()
    serializer_class = StudentSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = StudentFilter
    search_fields = ['first_name', 'last_name']
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(
    request=None,
    responses=ClassroomSerializer,
    parameters=[
        OpenApiParameter('name', description='Filter by classroom name', required=False, type=str),
        OpenApiParameter('semester', description='Filter by semester name', required=False, type=str),
    ],
    description="Retrieve classroom details, including teachers and students, with optional filters."
)
class ClassroomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Classroom.objects.prefetch_related('teachers', 'students', 'subject').all()
    serializer_class = ClassroomSerializer
    filter_backends = [filters.DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'semester__name']
    search_fields = ['name', 'subject__name']
    permission_classes = [permissions.IsAuthenticated]




# @extend_schema(
#     request=None,
#     responses=GradeSerializer,
#     parameters=[
#         OpenApiParameter('student__first_name', description='Filter by student first_name', required=False, type=int),
#         OpenApiParameter('student__last_name', description='Filter by student last_name', required=False, type=int),
#         OpenApiParameter('category__name', description='Filter by grade category name', required=False, type=str),
#     ],
#     description="Manage and view student grades with optional filters on student, classroom, and category."
# )
# class GradeViewSet(viewsets.ModelViewSet):
#     queryset = Grade.objects.all() 
#     serializer_class = GradeSerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     filterset_class = GradeFilter  
#     search_fields = ['student__first_name', 'student__last_name', 'classroom__name']
#     permission_classes = [permissions.IsAuthenticated]
