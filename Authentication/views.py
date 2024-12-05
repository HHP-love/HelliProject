from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .serializers import StudentSignupSerializer, AdminSignupSerializer, LoginSerializer, EmailSerializer


# Student Signup View
class StudentSignupView(APIView):

    @extend_schema(
        request=StudentSignupSerializer,
        responses={
            201: inline_serializer(
                name="StudentSignupSuccessResponse",
                fields={
                    "message": serializers.CharField(default="Student registration successful.")
                },
            ),
            400: inline_serializer(
                name="StudentSignupErrorResponse",
                fields={
                    "errors": serializers.DictField(child=serializers.CharField()),
                },
            ),
        },
        summary="Student Registration",
        description="Registers a new student with their full name, national code, and password.",
        tags=["Authentication"],
    )
    def post(self, request):
        serializer = StudentSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student registration successful."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Admin Signup View
class AdminSignupView(APIView):

    @extend_schema(
        request=AdminSignupSerializer,
        responses={
            201: inline_serializer(
                name="AdminSignupSuccessResponse",
                fields={
                    "message": serializers.CharField(default="Admin registration successful.")
                },
            ),
            400: inline_serializer(
                name="AdminSignupErrorResponse",
                fields={
                    "errors": serializers.DictField(child=serializers.CharField()),
                },
            ),
        },
        summary="Admin Registration",
        description="Registers a new admin with their full name and national code.",
        tags=["Authentication"],
    )
    def post(self, request):
        serializer = AdminSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Admin registration successful."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login View
class LoginView(APIView):

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: inline_serializer(
                name="LoginSuccessResponse",
                fields={
                    "refresh": serializers.CharField(),
                    "access": serializers.CharField(),
                    "role": serializers.CharField(),
                    "national_code": serializers.CharField(),
                },
            ),
            400: inline_serializer(
                name="LoginErrorResponse",
                fields={
                    "errors": serializers.CharField(default="Invalid credentials."),
                },
            ),
        },
        summary="User Login",
        description="Authenticates a user with national code and password, returning JWT tokens with role and national code.",
        tags=["Authentication"],
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            response = serializer.save()
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.http import JsonResponse

class LogoutView(APIView):
    def post(self, request):
        response = JsonResponse({"message": "Logged out successfully"})

        response.delete_cookie('refresh_token', httponly=True, secure=True, samesite='Strict')

        response.delete_cookie('access_token', httponly=True, secure=True, samesite='Strict')
        
        return response


# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication

class UserProfileView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        try:

            user = request.user
            profile_data = {
                "national_code": user.national_code,
                "role": user.role,
                "name": f"{user.first_name} {user.last_name}",
                "email": user.email,
            }
            return Response(profile_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "اطلاعات کاربر یافت نشد."}, status=status.HTTP_400_BAD_REQUEST)






from .models import Email
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class UpdateEmailView(APIView):
    """
    ویو برای به‌روزرسانی ایمیل کاربران بر اساس نقش.
    """

    def put(self, request):
        user = request.user

        if not user:
            return Response({"detail": "کاربر معتبر نیست."}, status=status.HTTP_400_BAD_REQUEST)


        # بررسی نقش کاربر
        if user.role not in ['Student', 'Admin']:
            return Response(
                {"detail": "نقش کاربر معتبر نیست."},
                status=status.HTTP_403_FORBIDDEN
            )

        # اعتبارسنجی ایمیل
        serializer = EmailSerializer(data=request.data)

        if not serializer.is_valid():
            print(f"Serializer Errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email')


        try:
            validate_email(email)  
        except ValidationError:
            return Response(
                {"detail": "ایمیل وارد شده معتبر نیست."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ذخیره یا به‌روزرسانی ایمیل در مدل Email
        try:
            email_obj, created = Email.objects.get_or_create(user=user)
            email_obj.email = email
            email_obj.is_verified = False  # ایمیل تایید نشده است
            email_obj.save()

            message = "ایمیل جدید ایجاد شد." if created else "ایمیل به‌روزرسانی شد."
            return Response(
                    {"detail": message},
                    status=status.HTTP_200_OK
                )

        except Exception as e:
            return Response(
                {"detail": f"خطای داخلی سرور: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
import random
from .models import EmailVerificationCode

class SendVerificationCodeView(APIView):
    def post(self, request):
        user = request.user
        try:
            email_instance = Email.objects.get(user=user)
        except Email.DoesNotExist:
            return Response({"error": "Email not found for this user."}, status=status.HTTP_404_NOT_FOUND)

        code = f"{random.randint(100000, 999999)}"
        expires_at = now() + timedelta(minutes=5)

        EmailVerificationCode.objects.create(mail=email_instance, code=code, expires_at=expires_at)

        send_mail(
            subject="Your Verification Code",
            message=f"Your verification code is {code}. It will expire in 5 minutes.",
            from_email="no-reply@example.com",
            recipient_list=[email_instance.email],
        )

        return Response({"message": "Verification code sent."}, status=status.HTTP_200_OK)
    

from .serializers import VerifyCodeSerializer

class VerifyCodeView(APIView):
    def post(self, request):
        user = request.user
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']

        if not code:
            return Response({"error": "Verification code is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            email_instance = Email.objects.get(user=user)
        except Email.DoesNotExist:
            return Response({"error": "Email not found for this user."}, status=status.HTTP_404_NOT_FOUND)

        try:
            verification_code = EmailVerificationCode.objects.get(mail=email_instance, code=code)
        except EmailVerificationCode.DoesNotExist:
            return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)


        if not verification_code.is_valid():
            verification_code.delete()  
            return Response({"error": "Verification code has expired."}, status=status.HTTP_400_BAD_REQUEST)

        email_instance.is_verified = True
        email_instance.save()

        EmailVerificationCode.objects.filter(mail=email_instance).delete()

        return Response({"message": "Email successfully verified."}, status=status.HTTP_200_OK)




