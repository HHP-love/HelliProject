from django.urls import path
from .views import AbsenceListView, AbsenceDetailView, RecordAbsenceView, AbsencePdfReportView, AbsenceHtmlReportView, documentation_view
from Grades.views import StudentListView

urlpatterns = [
    # نمایش لیست غیبت‌ها
    path('', AbsenceListView.as_view(), name='absence-list'),
    
    # ثبت غیبت جدید
    path('create/', RecordAbsenceView.as_view(), name='absence-create'),
    
    # جزئیات غیبت بر اساس کد ملی و تاریخ
    path('detail/<str:national_code>/<str:date>/', AbsenceDetailView.as_view(), name='absence-detail'),
    
    # گزارش PDF غیبت‌ها
    path('absences/pdf/', AbsencePdfReportView.as_view(), name='absence-pdf'),
    
    # گزارش HTML غیبت‌ها
    path('absences/html/', AbsenceHtmlReportView.as_view(), name='absence-html'),

    # نمایش لیست دانش‌آموزان
    path('students/', StudentListView.as_view(), name='student-list'),
    path('documentation/', documentation_view, name='documentation'),
]
