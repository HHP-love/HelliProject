from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .serializers import StudentSignupSerializer, AdminSignupSerializer, LoginSerializer
from django.urls import reverse
from .models import Student, Admin

# 


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
    




from rest_framework.generics import RetrieveUpdateAPIView
from django.core.exceptions import ObjectDoesNotExist
from .models import Email
from .serializers import EmailSerializer

class RegisterEmailView(RetrieveUpdateAPIView):
    """
    ویوی ثبت یا به‌روزرسانی ایمیل کاربر با استفاده از کد ملی
    """
    serializer_class = EmailSerializer


    def get_object(self):
        national_code = self.request.user.national_code
        try:
            email, created = Email.objects.get_or_create(user__national_code=national_code)
            return email
        except ObjectDoesNotExist:
            return None






# from .utils import verify_email_token

# class VerifyEmailView(APIView):
#     def get(self, request):
#         token = request.query_params.get('token')
#         user_id = verify_email_token(token)
#         if not user_id:
#             return Response({"error": "توکن نامعتبر است یا منقضی شده است."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = Student.objects.get(id=user_id) or Admin.objects.get(id=user_id)
#             user.is_email_verified = True
#             user.save()
#             return Response({"message": "ایمیل با موفقیت تأیید شد."}, status=status.HTTP_200_OK)
#         except (Student.DoesNotExist, Admin.DoesNotExist):
#             return Response({"error": "کاربر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)



# def send_verification_email(user):
#     token = generate_email_verification_token(user)
#     verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"  # لینک
#     subject = "تأیید ایمیل"
#     message = f"برای تأیید ایمیل خود روی لینک زیر کلیک کنید:\n{verification_url}"
#     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])