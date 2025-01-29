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
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import UpdateAPIView, ListAPIView

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

        queryset = queryset.prefetch_related('classrooms')  

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StudentDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOnly]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'slug'  # تغییر به slug به جای national_code

    @extend_schema(
        parameters=[
            OpenApiParameter("slug", OpenApiTypes.STR, description="The slug of the student to retrieve"),
        ]
    )
    def post(self, request, *args, **kwargs):
        student_slug = request.data.get("slug", None)  # دریافت slug به جای national_code

        if not student_slug:
            return Response({"detail": "Student slug is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            student = self.get_queryset().get(slug=student_slug)  # جستجو با استفاده از slug
        except Student.DoesNotExist:
            return Response({"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(student)
        return Response(serializer.data)



#endregion


#region semester

# class SemesterListView(generics.GenericAPIView):
#     permission_classes = [IsAuthenticated, IsAdminUserOnly]  
#     queryset = Semester.objects.all()
#     serializer_class = SemesterSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = SemesterFilter

#     @extend_schema(
#         parameters=[
#             OpenApiParameter("name", OpenApiTypes.STR, description="Search semesters by name"),
#             OpenApiParameter("start_date", OpenApiTypes.DATE, description="Filter semesters starting from a specific date"),
#             OpenApiParameter("end_date", OpenApiTypes.DATE, description="Filter semesters ending before a specific date"),
#         ]
#     )
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         queryset = Semester.objects.all()

#         # Apply filters if provided
#         name = data.get('name', None)
#         start_date = data.get('start_date', None)
#         end_date = data.get('end_date', None)

#         if name:
#             queryset = queryset.filter(name__icontains=name)
#         if start_date:
#             queryset = queryset.filter(start_date__gte=start_date)
#         if end_date:
#             queryset = queryset.filter(end_date__lte=end_date)

#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
class SemesterListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOnly]
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
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SemesterCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOnly]
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



from rest_framework import mixins

class SemesterUpdateDeleteView(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOnly]
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

# class SubjectListView(generics.GenericAPIView):
#     # permission_classes = [IsAuthenticated, IsAdminUserOnly]  
#     queryset = Subject.objects.all()
#     serializer_class = SubjectSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = SubjectFilter

#     @extend_schema(
#         parameters=[
#             OpenApiParameter("name", OpenApiTypes.STR, description="Search subjects by name"),
#             OpenApiParameter("code", OpenApiTypes.STR, description="Search subjects by code"),
#         ]
#     )
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         queryset = Subject.objects.all()

#         name = data.get('name', None)
#         code = data.get('code', None)

#         if name:
#             queryset = queryset.filter(name__icontains=name)
#         if code:
#             queryset = queryset.filter(code__exact=code)

#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

# class SubjectCreateView(generics.CreateAPIView):
#     # permission_classes = [IsAuthenticated, IsAdminUserOnly]  
#     queryset = Subject.objects.all()
#     serializer_class = SubjectSerializer

#     @extend_schema(
#         request=SubjectSerializer,
#         responses={201: SubjectSerializer}
#     )
#     def post(self, request, *args, **kwargs):
#         """
#         Create a new subject.
#         """
#         return self.create(request, *args, **kwargs)


# class SubjectUpdateDeleteView(generics.GenericAPIView, generics.mixins.UpdateModelMixin, generics.mixins.DestroyModelMixin):
#     # permission_classes = [IsAuthenticated, IsAdminUserOnly]  
#     queryset = Subject.objects.all()
#     serializer_class = SubjectSerializer
#     lookup_field = 'id' 

#     @extend_schema(
#         request=SubjectSerializer,
#         responses={200: SubjectSerializer}
#     )
#     def put(self, request, *args, **kwargs):
#         """
#         Update an existing subject by ID.
#         """
#         return self.update(request, *args, **kwargs)

#     @extend_schema(
#         parameters=[OpenApiParameter("id", OpenApiTypes.INT, description="The ID of the subject to delete")]
#     )
#     def delete(self, request, *args, **kwargs):
#         """
#         Delete an existing subject by ID.
#         """
#         return self.destroy(request, *args, **kwargs)

class SubjectListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUserOnly]
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
    def get(self, request, *args, **kwargs):
        """
        Filter subjects by name or code using GET.
        """
        queryset = self.get_queryset()

        # Apply filters if provided
        name = request.GET.get('name', None)
        code = request.GET.get('code', None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if code:
            queryset = queryset.filter(code__exact=code)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SubjectCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUserOnly]
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
    permission_classes = [IsAuthenticated, IsAdminUserOnly]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    lookup_field = 'slug'  # Using slug instead of id for better user-friendly URLs

    @extend_schema(
        request=SubjectSerializer,
        responses={200: SubjectSerializer}
    )
    def put(self, request, *args, **kwargs):
        """
        Update an existing subject by slug.
        """
        return self.update(request, *args, **kwargs)

    @extend_schema(
        parameters=[OpenApiParameter("slug", OpenApiTypes.STR, description="The slug of the subject to delete")]
    )
    def delete(self, request, *args, **kwargs):
        """
        Delete an existing subject by slug.
        """
        return self.destroy(request, *args, **kwargs)


#endregion


#region classroom


class ClassroomListView(generics.GenericAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    filter_backends = (DjangoFilterBackend,)  
    filterset_class = ClassroomFilter 
    # permission_classes = [IsAuthenticated, IsAdminUserOnly]

    def post(self, request, *args, **kwargs):
        """
        این متد POST فیلترهای پیچیده و پیشرفته را از طریق بدنه درخواست دریافت می‌کند
        و بر اساس آن‌ها داده‌ها را فیلتر می‌کند.
        """

        data = request.data
        queryset = self.queryset

        name = data.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)

        teachers = data.get('teachers', None)
        if teachers:
            queryset = queryset.filter(teachers__id__in=teachers)

        students = data.get('students', None)
        if students:
            queryset = queryset.filter(students__id__in=students)

        subject = data.get('subject', None)
        if subject:
            queryset = queryset.filter(subject__id=subject)

        start_time = data.get('start_time', None)
        if start_time:
            queryset = queryset.filter(start_time__gte=start_time)

        end_time = data.get('end_time', None)
        if end_time:
            queryset = queryset.filter(end_time__lte=end_time)

        filtered_queryset = self.filter_queryset(queryset)

        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)



class ClassroomCreateView(generics.CreateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomCreateUpdateSerializer
    # permission_classes = [IsAuthenticated, IsAdminUserOnly]


class ClassroomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classroom.objects.all()
    # permission_classes = [IsAuthenticated, IsAdminUserOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ClassroomCreateUpdateSerializer
        return ClassroomSerializer
    
#endregion


#region grades

class GradeCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOnly]  

    def post(self, request, *args, **kwargs):
        serializer = GradeSerializer(data=request.data)

        if serializer.is_valid():
            grade = serializer.save(recorded_by=request.user)  # ذخیره نمره و ثبت معلم به عنوان کسی که نمره را ثبت کرده است
            return Response({"message": _("Grade successfully created"), "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GradeUpdateView(UpdateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeUpdateSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can update grades

    def update(self, request, *args, **kwargs):
        """
        Override the update method to track changes and store history.
        """
        instance = self.get_object()  # Retrieve the grade instance to be updated
        old_score = instance.score

        # Validate that the new score does not exceed the maximum score
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_grade = serializer.save()

        # Create a history record if the score was changed
        if updated_grade.score != old_score:
            GradeHistory.objects.create(
                grade=updated_grade,
                changed_by=request.user,  # assuming request.user is the teacher
                old_score=old_score,
                new_score=updated_grade.score,
                reason_for_change=request.data.get('reason_for_change', ''),
            )

        return Response(serializer.data, status=status.HTTP_200_OK)


class GradeListView(ListAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    # permission_classes = [IsAuthenticated] 
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GradeFilter
    pagination_class = None


class CompareGradesView(APIView):
    permission_classes = [IsAuthenticated] #TODO 12

    def get(self, request, student_id):
        grades = Grade.objects.filter(student__id=student_id)
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)
    

class GPAView(APIView):
    def get(self, request, student_id, semester_id):
        try:
            gpa_record = GPA.objects.get(student_id=student_id, semester_id=semester_id)
        except GPA.DoesNotExist:
            return Response({"detail": "GPA record not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = GPASerializer(gpa_record)
        return Response(serializer.data)
    
class CompareGPAView(APIView):
    def get(self, request, student_id):
        gpas = GPA.objects.filter(student_id=student_id)
        gpa_data = []

        for gpa in gpas:
            gpa_data.append({
                'semester': gpa.semester.name,
                'gpa': gpa.calculated_gpa
            })

        return Response(gpa_data)

class GPAListView(APIView):
    def get(self, request):
        student_id = request.query_params.get('student', None)
        semester_id = request.query_params.get('semester', None)
        classroom_id = request.query_params.get('classroom', None)

        gpas = GPA.objects.all()

        if student_id:
            gpas = gpas.filter(student_id=student_id)
        if semester_id:
            gpas = gpas.filter(semester_id=semester_id)
        if classroom_id:
            gpas = gpas.filter(student__classroom_id=classroom_id)

        serializer = GPAListSerializer(gpas, many=True)
        return Response(serializer.data)
    
class GPAHistoryView(APIView):
    def get(self, request, gpa_id):
        gpa_history = GPAHistory.objects.filter(gpa_record_id=gpa_id)

        if not gpa_history:
            return Response({"detail": "History not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = GPAHistorySerializer(gpa_history, many=True)
        return Response(serializer.data)
#endregion




