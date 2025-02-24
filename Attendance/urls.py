from django.urls import path
from .views import AbsenceListView, AbsenceDetailView, RecordAbsenceView, AbsencePdfReportView, AbsenceHtmlReportView
from Grades.views import StudentListView
urlpatterns = [
    path('', AbsenceListView.as_view(), name='absence-list'),
    path('create/', RecordAbsenceView.as_view(), name='absence-list'),
    path('detail/<str:national_code>/<str:date>/', AbsenceDetailView.as_view(), name='detail-absence'),
    path('absences/pdf/', AbsencePdfReportView.as_view(), name='absence_pdf'),
    path('absences/html/', AbsenceHtmlReportView.as_view(), name='absence_pdf'),
    path('students/', StudentListView.as_view(), name='absence_pdf'),
]
