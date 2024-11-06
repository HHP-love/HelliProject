
# Create your views here.
from django.shortcuts import render
from rest_framework import generics, mixins
from .models import Absence, Student
from .serializers import AbsenceSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema,OpenApiParameter, OpenApiTypes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

#region AbsenceListView

@extend_schema(
    summary="Retrieve a list of absences",
    description=(
        "This endpoint retrieves a list of all absence records in the system. "
        "You can apply filters based on student details such as name, grade, and national code, "
        "as well as the absence date and presence status. "
        "The response is paginated and includes a detailed list of absences."
    ),
    parameters=[
        OpenApiParameter(
            name='student__name', 
            description="Filter absences by the student's name (partial match allowed).",
            required=False,
            type=OpenApiTypes.STR
        ),
        OpenApiParameter(
            name='student__grade', 
            description="Filter absences by the student's grade (exact match).",
            required=False,
            type=OpenApiTypes.INT
        ),
        OpenApiParameter(
            name='student__national_code', 
            description="Filter absences by the student's unique national code.",
            required=False,
            type=OpenApiTypes.STR
        ),
        OpenApiParameter(
            name='date', 
            description="Filter absences by the date of absence (in YYYY-MM-DD format).",
            required=False,
            type=OpenApiTypes.DATE
        ),
        OpenApiParameter(
            name='is_present', 
            description="Filter absences based on the presence status (True for present, False for absent).",
            required=False,
            type=OpenApiTypes.BOOL
        ),
    ],
    responses={
        200: AbsenceSerializer(many=True),
        400: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT,
    }
)
class AbsenceListView(generics.ListAPIView):
    queryset = Absence.objects.all()
    serializer_class = AbsenceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student__first_name', 'student__last_name','student__grade', 'student__national_code', 'date', 'status']

#endregion



#region AbsenceDetailView

class AbsenceDetailView(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    serializer_class = AbsenceSerializer


    @extend_schema(
        summary="Update an absence record",
        description=(
            "Update an existing absence record. "
            "Provide the student's national code and the date of the absence. "
            "Include the fields to be updated in the request body."
        ),
        request=AbsenceSerializer,
        responses={
            200: AbsenceSerializer,
            400: OpenApiTypes.OBJECT,
        }
    )
    def put(self, request, *args, **kwargs):
        absence = self.get_object()
        serializer = AbsenceSerializer(absence, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete an absence record",
        description=(
            "Delete an absence record for a student based on their national code and date. "
            "This action is irreversible."
        ),
        responses={
            204: None,
            404: OpenApiTypes.OBJECT,
        }
    )
    def delete(self, request, *args, **kwargs):
        absence = self.get_object()
        absence.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#endregion    



#region AbsenceCreateView

# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student, Absence
from .serializers import AbsenceSerializer
from django.utils.dateparse import parse_date

class RecordAbsenceView(APIView):
    """
    ویو برای ثبت غیبت دانش‌آموز بر اساس کد ملی و تاریخ.
    """

    def post(self, request, *args, **kwargs):
        national_code = request.data.get("national_code")
        date_str = request.data.get("date")
        
        # بررسی وجود کد ملی و تاریخ
        if not national_code or not date_str:
            return Response(
                {"error": "کد ملی و تاریخ باید ارسال شوند."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # تبدیل تاریخ از رشته به فرمت Date
        try:
            date = parse_date(date_str)
            if date is None:
                raise ValueError("تاریخ نامعتبر است.")
        except ValueError:
            return Response({"error": "فرمت تاریخ نادرست است. از YYYY-MM-DD استفاده کنید."},
                            status=status.HTTP_400_BAD_REQUEST)

        # بررسی وجود دانش‌آموز با کد ملی
        try:
            student = Student.objects.get(national_code=national_code)
        except Student.DoesNotExist:
            return Response(
                {"error": "دانش‌آموزی با این کد ملی یافت نشد."},
                status=status.HTTP_404_NOT_FOUND
            )

        # بررسی عدم تکرار غیبت برای همان تاریخ
        if Absence.objects.filter(student=student, date=date).exists():
            return Response(
                {"error": "این دانش‌آموز در این تاریخ قبلاً ثبت شده است."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ثبت غیبت
        absence = Absence.objects.create(student=student, date=date, status="absence")
        serializer = AbsenceSerializer(absence)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


