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
    


from rest_framework_simplejwt.authentication import JWTAuthentication



# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Email, Student, Admin
from .serializers import EmailSerializer  
from rest_framework.permissions import IsAuthenticated


# class UpdateEmailView(APIView):

#     def put(self, request):
#         user = request.user

#         # Validate the email from the request
#         serializer = EmailSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         # Check if the user is an instance of Student or Admin
#         if hasattr(user, 'student'):  # Check if user has an associated Student
#             user_type = 'Student'
#         elif hasattr(user, 'admin'):  # Check if user has an associated Admin
#             user_type = 'Admin'
#         else:
#             return Response({"detail": "کاربر معتبر نیست."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Try to get the associated email
#             user_email = Email.objects.get(user=user)
#             # Update email if it exists
#             user_email.email = email
#             user_email.is_verified = False  # or handle verification differently
#             user_email.save()
#             return Response({"detail": "ایمیل با موفقیت به‌روزرسانی شد."}, status=status.HTTP_200_OK)
#         except Email.DoesNotExist:
#             # If the email does not exist, create a new one
#             Email.objects.create(user=user, email=email, is_verified=False)
#             return Response({"detail": "ایمیل جدید با موفقیت ثبت شد."}, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response({"detail": f"یک خطا رخ داد: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


from django.contrib.contenttypes.models import ContentType


from .serializers import EmailSerializer
from .models import Email

class UpdateEmailView(APIView):
    """
    ویو برای به‌روزرسانی ایمیل کاربران بر اساس نقش.
    """


    def put(self, request):
        user = request.user

        print(f"User: {user}")
        print(f"User Type: {type(user)}")  # چاپ نوع واقعی user
        # بررسی نقش کاربر
        if user.role not in ['Student', 'Admin']:
            return Response(
                {"detail": "نقش کاربر معتبر نیست."},
                status=status.HTTP_403_FORBIDDEN
            )

        # اعتبارسنجی ایمیل
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
