# urls.py
from django.urls import path
from .views import StudentSignupView, LoginView , AdminSignupView, UpdateEmailView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('signup/student/', StudentSignupView.as_view(), name='student-signup'),
    path('signup/admin/', AdminSignupView.as_view(), name='admin_signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login-refresh'),
    path('update-email/', UpdateEmailView.as_view(), name='update_email'),
]

