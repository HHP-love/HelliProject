# urls.py
from django.urls import path
from .views import (
    StudentSignupView, LoginView , AdminSignupView, UpdateEmailView, SendVerificationCodeView, 
    VerifyCodeView, LogoutView, UserProfileView
    )
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path



urlpatterns = [
    path('signup/student/', StudentSignupView.as_view(), name='student-signup'),
    path('signup/admin/', AdminSignupView.as_view(), name='admin_signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login-refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user-profile/', LogoutView.as_view(), name='user-profile'),
    path('update-email/', UpdateEmailView.as_view(), name='update_email'),
    path('send-verification-code/', SendVerificationCodeView.as_view(), name='send_verification_code'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify_code'),
]

