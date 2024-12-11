from django.urls import path
from .views import *

urlpatterns = [
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/detail/', StudentDetailView.as_view(), name='student-detail'),

    path('semesters/', SemesterListView.as_view(), name='semester-list'),
    path('semesters/<int:id>/', SemesterUpdateDeleteView.as_view(), name='semester-update-delete'),
    path('semesters/create/', SemesterCreateView.as_view(), name='semester-create'),

    path('subjects/list/', SubjectListView.as_view(), name='subject-filter'),
    path('subjects/create/', SubjectCreateView.as_view(), name='subject-create'),
    path('subjects/update-delete/<int:id>/', SubjectUpdateDeleteView.as_view(), name='subject-update-delete'),
]