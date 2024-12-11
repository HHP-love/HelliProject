# views.py

#region imports

from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from .permissions import IsAdminUserOnly
from .filters import *
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django_filters.rest_framework import DjangoFilterBackend

#endregion


#region student information

class StudentListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOnly]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @extend_schema(
        request=OpenApiTypes.OBJECT,
        parameters=[
            OpenApiParameter("first_name", OpenApiTypes.STR, description="Search students by first name"),
            OpenApiParameter("last_name", OpenApiTypes.STR, description="Search students by last name"),
            OpenApiParameter("national_code", OpenApiTypes.STR, description="Search students by national code"),
            OpenApiParameter("grade", OpenApiTypes.INT, description="Search students by grade"),
        ]
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        queryset = Student.objects.all()
        
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        national_code = data.get('national_code', None)
        grade = data.get('grade', None)

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if national_code:
            queryset = queryset.filter(national_code__exact=national_code)
        if grade:
            queryset = queryset.filter(grade=grade)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StudentDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOnly]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'national_code'  

    @extend_schema(
        parameters=[
            OpenApiParameter("national_code", OpenApiTypes.STR, description="The national_code of the student to retrieve"),
        ]
    )
    def post(self, request, *args, **kwargs):
        student_national_code = request.data.get("national_code", None)  

        if not student_national_code:
            return Response({"detail": "Student national_code is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            student = self.get_queryset().get(national_code=student_national_code)  
        except Student.DoesNotExist:
            return Response({"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(student)
        return Response(serializer.data)


#endregion


#region semester

class SemesterListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUserOnly]  
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SemesterFilter

    @extend_schema(
        parameters=[
            OpenApiParameter("name", OpenApiTypes.STR, description="Search semesters by name"),
            OpenApiParameter("start_date", OpenApiTypes.DATE, description="Filter semesters starting from a specific date"),
            OpenApiParameter("end_date", OpenApiTypes.DATE, description="Filter semesters ending before a specific date"),
        ]
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        queryset = Semester.objects.all()

        # Apply filters if provided
        name = data.get('name', None)
        start_date = data.get('start_date', None)
        end_date = data.get('end_date', None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SemesterCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUserOnly]
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer

    @extend_schema(
        request=SemesterSerializer,
        responses={201: SemesterSerializer}
    )
    def post(self, request, *args, **kwargs):
        """
        Create a new semester.
        """
        return self.create(request, *args, **kwargs)


class SemesterUpdateDeleteView(generics.GenericAPIView, generics.mixins.UpdateModelMixin, generics.mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated, IsAdminUserOnly]
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    lookup_field = 'id'

    @extend_schema(
        request=SemesterSerializer,
        responses={200: SemesterSerializer}
    )
    def put(self, request, *args, **kwargs):
        """
        Update an existing semester by ID.
        """
        return self.update(request, *args, **kwargs)

    @extend_schema(
        parameters=[OpenApiParameter("id", OpenApiTypes.INT, description="The ID of the semester to delete")]
    )
    def delete(self, request, *args, **kwargs):
        """
        Delete an existing semester by ID.
        """
        return self.destroy(request, *args, **kwargs)


#endregion


#region subject

class SubjectListView(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUserOnly]  
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SubjectFilter

    @extend_schema(
        parameters=[
            OpenApiParameter("name", OpenApiTypes.STR, description="Search subjects by name"),
            OpenApiParameter("code", OpenApiTypes.STR, description="Search subjects by code"),
        ]
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        queryset = Subject.objects.all()

        name = data.get('name', None)
        code = data.get('code', None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if code:
            queryset = queryset.filter(code__exact=code)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class SubjectCreateView(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUserOnly]  
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    @extend_schema(
        request=SubjectSerializer,
        responses={201: SubjectSerializer}
    )
    def post(self, request, *args, **kwargs):
        """
        Create a new subject.
        """
        return self.create(request, *args, **kwargs)


class SubjectUpdateDeleteView(generics.GenericAPIView, generics.mixins.UpdateModelMixin, generics.mixins.DestroyModelMixin):
    # permission_classes = [IsAuthenticated, IsAdminUserOnly]  
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    lookup_field = 'id' 

    @extend_schema(
        request=SubjectSerializer,
        responses={200: SubjectSerializer}
    )
    def put(self, request, *args, **kwargs):
        """
        Update an existing subject by ID.
        """
        return self.update(request, *args, **kwargs)

    @extend_schema(
        parameters=[OpenApiParameter("id", OpenApiTypes.INT, description="The ID of the subject to delete")]
    )
    def delete(self, request, *args, **kwargs):
        """
        Delete an existing subject by ID.
        """
        return self.destroy(request, *args, **kwargs)

#endregion


