# urls.py

from django.urls import path
from .views import (
    GradeListCreateView, GradeRetrieveUpdateDestroyView,
    SchoolClassListCreateView, SchoolClassRetrieveUpdateDestroyView,
    SubjectListCreateView, SubjectRetrieveUpdateDestroyView,
    TeacherListCreateView, TeacherRetrieveUpdateDestroyView,
    DayListCreateView, DayRetrieveUpdateDestroyView,
    PeriodListCreateView, PeriodRetrieveUpdateDestroyView,
    ScheduleListCreateView, ScheduleRetrieveUpdateDestroyView
)

urlpatterns = [
    # Grade URLs
    path('grades/', GradeListCreateView.as_view(), name='grade-list-create'),
    path('grades/<int:pk>/', GradeRetrieveUpdateDestroyView.as_view(), name='grade-retrieve-update-destroy'),

    # SchoolClass URLs
    path('school-classes/', SchoolClassListCreateView.as_view(), name='school-class-list-create'),
    path('school-classes/<int:pk>/', SchoolClassRetrieveUpdateDestroyView.as_view(), name='school-class-retrieve-update-destroy'),

    # Subject URLs
    path('subjects/', SubjectListCreateView.as_view(), name='subject-list-create'),
    path('subjects/<int:pk>/', SubjectRetrieveUpdateDestroyView.as_view(), name='subject-retrieve-update-destroy'),

    # Teacher URLs
    path('teachers/', TeacherListCreateView.as_view(), name='teacher-list-create'),
    path('teachers/<int:pk>/', TeacherRetrieveUpdateDestroyView.as_view(), name='teacher-retrieve-update-destroy'),

    # Day URLs
    path('days/', DayListCreateView.as_view(), name='day-list-create'),
    path('days/<int:pk>/', DayRetrieveUpdateDestroyView.as_view(), name='day-retrieve-update-destroy'),

    # Period URLs
    path('periods/', PeriodListCreateView.as_view(), name='period-list-create'),
    path('periods/<int:pk>/', PeriodRetrieveUpdateDestroyView.as_view(), name='period-retrieve-update-destroy'),

    # Schedule URLs
    path('schedules/', ScheduleListCreateView.as_view(), name='schedule-list-create'),
    path('schedules/<int:pk>/', ScheduleRetrieveUpdateDestroyView.as_view(), name='schedule-retrieve-update-destroy'),
]
