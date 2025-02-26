from django.urls import path
from .views import AbsenceListView, GetAbsencesByNationalCodeView, RecordAbsenceView, AbsencePdfReportView, AbsenceHtmlReportView, documentation_view
from Grades.views import StudentListView

urlpatterns = [
    # نمایش لیست غیبت‌ها
    path('', AbsenceListView.as_view(), name='absence-list'),
    
    # ثبت غیبت جدید
    path('create/', RecordAbsenceView.as_view(), name='absence-create'),
    
    #جزئیات غیبت بر اساس کد ملی 
    path('detail/<str:national_code>/', GetAbsencesByNationalCodeView.as_view(), name='absence-detail'),
    
    # گزارش PDF غیبت‌ها
    path('absences/pdf/', AbsencePdfReportView.as_view(), name='absence-pdf'),
    
    # گزارش HTML غیبت‌ها
    path('absences/html/', AbsenceHtmlReportView.as_view(), name='absence-html'),

    # نمایش لیست دانش‌آموزان
    path('students/', StudentListView.as_view(), name='student-list'),
    path('documentation/', documentation_view, name='documentation'),
]
