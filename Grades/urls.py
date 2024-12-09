from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.views_v1 import TeacherViewSet, StudentViewSet, ClassroomViewSet #, GradeViewSet

router_1 = DefaultRouter()
router_1.register(r'teachers', TeacherViewSet)
router_1.register(r'students', StudentViewSet)
router_1.register(r'classrooms', ClassroomViewSet)
# router_1.register(r'grades', GradeViewSet)

urlpatterns = [
    path('v1/', include(router_1.urls)),
]
