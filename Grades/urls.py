from django.urls import path
from .views import *

urlpatterns = [
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/detail/<slug:slug>/', StudentDetailView.as_view(), name='student-detail'),

    path('semesters/', SemesterListView.as_view(), name='semester-list'),
    path('semesters/<int:id>/', SemesterUpdateDeleteView.as_view(), name='semester-update-delete'),
    path('semesters/create/', SemesterCreateView.as_view(), name='semester-create'),

    path('subjects/', SubjectListView.as_view(), name='subject-list'),  
    path('subjects/create/', SubjectCreateView.as_view(), name='subject-create'),  
    path('subjects/<slug:slug>/', SubjectUpdateDeleteView.as_view(), name='subject-update-delete'), 

    path('classrooms/', ClassroomListView.as_view(), name='classroom-list'),
    path('classrooms/create/', ClassroomCreateView.as_view(), name='classroom-create'),
    path('classrooms/detail/<int:pk>/', ClassroomDetailView.as_view(), name='classroom-detail'),

    path('list/', GradeListView.as_view(), name='grade-list'),
    path('create/', GradeCreateView.as_view(), name='grade-create'),
    path('update/<int:pk>', GradeUpdateView.as_view(), name='grade-update'),
    path('compare-grades/<int:student_id>/', CompareGradesView.as_view(), name='compare-grades'),
    path('gpa/<int:student_id>/<int:semester_id>/', GPAView.as_view(), name='gpa_view'),
    path('compare-gpa/<int:student_id>/', CompareGPAView.as_view(), name='compare_gpa_view'),
    path('gpa-list/', GPAListView.as_view(), name='gpa_list_view'),
    path('gpa-history/<int:gpa_id>/', GPAHistoryView.as_view(), name='gpa_history_view'),
]