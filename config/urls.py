
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView, SpectacularJSONAPIView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #apps
    path('attendance/', include('Attendance.urls')),
    path('authentication/', include('Authentication.urls')),
    path('survay/', include('Survey.urls')),
    path('weekly-schedule/', include('WeeklySchedule.urls')),
    path('grades/', include('WeeklySchedule.urls')),

    #swagger and test
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('test/', views.send_email_view),
    path('redoc/', views.redoc_view, name='redoc'),
]

