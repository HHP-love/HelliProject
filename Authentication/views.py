from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .serializers import StudentSignupSerializer, AdminSignupSerializer, LoginSerializer
from django.urls import reverse


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
            tokens = serializer.save()
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




from .models import Email

from .serializers import EmailSerializer
from .models import Email

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import EmailSerializer
from .models import Email
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmailSerializer
from .models import Email
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmailSerializer
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

        # بررسی وضعیت request.data
        print(f"Request Data: {request.data}")

        # اعتبارسنجی ایمیل
        serializer = EmailSerializer(data=request.data)

        # چاپ داده‌های Serializer برای دیباگ
        print(f"Serializer Data: {serializer.initial_data}")  # مشاهده داده‌های اولیه

        if not serializer.is_valid():
            print(f"Serializer Errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email')


        try:
            validate_email(email)  # اعتبارسنجی ایمیل
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
            print(email_obj)
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




