from django_filters import rest_framework as filters
from rest_framework import generics, mixins
from .models import Absence
from Grades.models import Student
from .serializers import AbsenceSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema,OpenApiParameter, OpenApiTypes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

#region AbsenceListView
from .filters import AbsenceFilter
class AbsenceListView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        queryset = Absence.objects.all()
        filterset = AbsenceFilter(data, queryset=queryset)
        if not filterset.is_valid():
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = AbsenceSerializer(filterset.qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

#endregion

#region AbsenceDetailView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Absence, Student
from .serializers import AbsenceSerializer

class GetAbsencesByNationalCodeView(APIView):
    """
    ویو برای دریافت تمامی غیبت‌ها برای یک دانش‌آموز بر اساس کد ملی.
    """

    def get(self, request, national_code, *args, **kwargs):
        # بررسی وجود دانش‌آموز با کد ملی
        try:
            student = Student.objects.get(national_code=national_code)
        except Student.DoesNotExist:
            return Response({"error": "دانش‌آموزی با این کد ملی یافت نشد."}, status=status.HTTP_404_NOT_FOUND)


        absences = Absence.objects.filter(student=student)

        if not absences.exists():
            return Response({"message": "هیچ غیبی برای این دانش‌آموز ثبت نشده است."}, status=status.HTTP_200_OK)

        serializer = AbsenceSerializer(absences, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



    
#endregion    



#region AbsenceCreateView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Absence, Student
from .serializers import AbsenceSerializer
from django.utils.dateparse import parse_date

class RecordAbsenceView(APIView):
    """
    ویو برای ثبت یا ویرایش غیبت‌های گروهی دانش‌آموزان بر اساس کد ملی و تاریخ.
    """

    def put(self, request, *args, **kwargs):
        absences = request.data.get("absences", [])
        
        if not absences:
            return Response({"error": "لیست غیبت‌ها نمی‌تواند خالی باشد."}, status=status.HTTP_400_BAD_REQUEST)

        processed_absences = []  # برای ذخیره غیبت‌های ثبت یا ویرایش شده

        for absence_data in absences:
            national_code = absence_data.get("national_code")
            date_str = absence_data.get("date")
            absence_status = absence_data.get("status")
            
            # بررسی وجود کد ملی، تاریخ و وضعیت
            if not national_code or not date_str or not absence_status:
                processed_absences.append({"error": "کد ملی، تاریخ و وضعیت باید ارسال شوند."})
                continue

            # تبدیل تاریخ از رشته به فرمت Date
            try:
                date = parse_date(date_str)
                if date is None:
                    raise ValueError("تاریخ نامعتبر است.")
            except ValueError:
                processed_absences.append({"error": "فرمت تاریخ نادرست است. از YYYY-MM-DD استفاده کنید."})
                continue

            try:
                student = Student.objects.get(national_code=national_code)
            except Student.DoesNotExist:
                processed_absences.append({"error": "دانش‌آموزی با این کد ملی یافت نشد."})
                continue

            # بررسی اگر غیبت قبلاً ثبت شده باشد و ویرایش آن یا ثبت غیبت جدید
            absence, created = Absence.objects.update_or_create(
                student=student,
                date=date,
                defaults={'status': absence_status}
            )

            # اگر غیبت جدید باشد، ایجاد آن را ثبت می‌کنیم
            if created:
                processed_absences.append({"message": "غیبت جدید ثبت شد.", "data": AbsenceSerializer(absence).data})
            else:
                processed_absences.append({"message": "غیبت قبلی ویرایش شد.", "data": AbsenceSerializer(absence).data})

        # بازگرداندن تمامی غیبت‌ها که ثبت یا ویرایش شده‌اند
        return Response(processed_absences, status=status.HTTP_200_OK)





from django.http import JsonResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings
import os

class AbsencePdfReportView(APIView):
    """
    ویو برای دریافت گزارش PDF از غیبت‌ها با فیلترهای مختلف.
    """

    def post(self, request, *args, **kwargs):
        data = request.data
        queryset = Absence.objects.all()

        filterset = AbsenceFilter(data, queryset=queryset)
        if not filterset.is_valid():
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        absences = filterset.qs
        absence_data = AbsenceSerializer(absences, many=True).data

        html_filename = 'absence_report.html'
        html_path = os.path.join(settings.MEDIA_ROOT, html_filename)

        html_content = render_to_string('absence_report_template.html', {'absences': absence_data})

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        pdf_filename = 'absence_report.pdf'
        pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_filename)

        HTML(string=html_content).write_pdf(pdf_path)

        file_url = os.path.join(settings.MEDIA_URL, pdf_filename)

        return JsonResponse({"file_url": file_url})




from django.shortcuts import render
from django.http import HttpResponse
from .models import Absence
from .serializers import AbsenceSerializer
from django.template.loader import render_to_string
from .filters import AbsenceFilter
from django.conf import settings
import os

class AbsenceHtmlReportView(APIView):
    """
    ویو برای دریافت گزارش HTML از غیبت‌ها با فیلترهای مختلف.
    """

    def post(self, request, *args, **kwargs):
        data = request.data
        queryset = Absence.objects.all()

        filterset = AbsenceFilter(data, queryset=queryset)
        if not filterset.is_valid():
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        absences = filterset.qs
        absence_data = AbsenceSerializer(absences, many=True).data

        html_filename = 'absence_report.html'
        html_path = os.path.join(settings.MEDIA_ROOT, html_filename)
        html_content = render_to_string('absence_report_template.html', {'absences': absence_data})

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        file_url = os.path.join(settings.MEDIA_URL, html_filename)

        return JsonResponse({"file_url": file_url})


from django.shortcuts import render

def documentation_view(request):
    """
    این view صفحه مستندات API را رندر می‌کند.
    """
    return render(request, 'attendance-documentation.html')