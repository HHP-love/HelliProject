from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .serializers import * 
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from .models import *

#region signup

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

#endregion

#region login

# Login View

from django.http import JsonResponse
from django.conf import settings
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
            response_data = serializer.save()
            response = JsonResponse(response_data)
            
            # تنظیم کوکی‌ها
            response.set_cookie(
                'refresh_token', response_data['refresh'],
                httponly=True, secure=False if settings.DEBUG else True, samesite='Lax'
            )
            response.set_cookie(
                'access_token', response_data['access'],
                httponly=True, secure=False if settings.DEBUG else True, samesite='Lax'
            )
            
            response['Authorization'] = f"Bearer {response_data['access']}"
            return response
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#endregion

#region logout

class LogoutView(APIView):
    def post(self, request):
        response = JsonResponse({"message": "Logged out successfully"})

        response.delete_cookie('refresh_token', samesite='Strict')

        response.delete_cookie('access_token',samesite='Strict')
        
        return response


#endregion

#region UserProfile

from rest_framework_simplejwt.authentication import JWTAuthentication

class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.headers)
        try:

            user = request.user
            profile_data = {
                "national_code": user.national_code,
                "role": user.role,
                "name": f"{user.first_name} {user.last_name}",
            }
            print(profile_data)
            return Response(profile_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(user)
            return Response({"error": "اطلاعات کاربر یافت نشد."}, status=status.HTTP_400_BAD_REQUEST)


#endregion



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



from django.utils.timezone import now
from datetime import timedelta
import random
from .models import EmailVerificationCode
from .throttles import SendVerificationCodeThrottle
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

class SendVerificationCodeView(APIView):
    throttle_classes = [SendVerificationCodeThrottle]
    def post(self, request):
        user = request.user
        try:
            email_instance = Email.objects.get(user=user)
        except Email.DoesNotExist:
            return Response({"error": "An error occurred."}, status=status.HTTP_400_BAD_REQUEST)

        code = f"{random.randint(100000, 999999)}"
        expires_at = now() + timedelta(minutes=5)

        EmailVerificationCode.objects.filter(mail=email_instance).delete()
        verification_code = EmailVerificationCode(mail=email_instance, expires_at=expires_at)
        verification_code.set_code(code)
        verification_code.save()
        

        html_content = render_to_string('emails/verification_code.html', {
            'user_name': user.first_name + user.last_name,
            'code': code,
            'national_code' : user.national_code,
        })


        subject = "Your Verification Code"
        from_email = "admin@gmail.com"
        recipient_list = [email_instance.email]

        email = EmailMultiAlternatives(subject, "Your verification code is in the HTML version.", from_email, recipient_list)
        email.attach_alternative(html_content, "text/html")
        email.send()

        return Response({"message": "Verification code sent."}, status=status.HTTP_200_OK)
    
from .serializers import VerifyCodeSerializer

class VerifyCodeView(APIView):
    def post(self, request):
        user = request.user
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        raw_code = serializer.validated_data['code']

        try:
            email_instance = Email.objects.get(user=user)
            verification_code = EmailVerificationCode.objects.get(mail=email_instance)
        except (Email.DoesNotExist, EmailVerificationCode.DoesNotExist):
            return Response({"error": "An error occurred."}, status=status.HTTP_400_BAD_REQUEST)

        if not verification_code.verify_code(raw_code) or not verification_code.is_valid():
            if verification_code.attempts >= 5:
                return Response({"error": "Too many attempts. Please request a new code."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

            verification_code.attempts += 1
            
            verification_code.save()
            return Response({"error": "Invalid or expired verification code."}, status=status.HTTP_400_BAD_REQUEST)

        email_instance.is_verified = True
        email_instance.save()
        verification_code.delete()

        return Response({"message": "Email successfully verified."}, status=status.HTTP_200_OK)




from django.core.exceptions import ObjectDoesNotExist

class ChangePassword(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    throttle_classes = [SendVerificationCodeThrottle]


    @extend_schema(
        summary="Change password",
        description="This endpoint allows the authenticated user or an admin to change the password."
                    " The user must provide the current password and a new password."
                    " Admin users can update the password for any user if they have the correct credentials.",
        request=ChangePasswordSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Password successfully updated.",
                examples=[{
                    "application/json": {
                        "message": "Password updated successfully."
                    }
                }]
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Bad request, invalid data or incorrect previous password.",
                examples=[{
                    "application/json": {
                        "error": "Incorrect previous password."
                    }
                }]
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="User not found.",
                examples=[{
                    "application/json": {
                        "error": "User not found."
                    }
                }]
            )
        },
        parameters=[
            OpenApiParameter(
                name='previous_password',
                type=str,
                required=True,
                description="The current password of the user."
            ),
            OpenApiParameter(
                name='new_password',
                type=str,
                required=True,
                description="The new password to be set."
            )
        ]
    )
    def patch(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserBase.objects.get(national_code=request.user.national_code)
        except ObjectDoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        previous_password = serializer.validated_data['previous_password']
        new_password = serializer.validated_data['new_password']

        if not user.check_password(previous_password):
            return Response({"error": "Incorrect previous password."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import NotFound
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import PasswordResetCode, Email
from .serializers import EmailSerializer


class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]  
    throttle_classes = [SendVerificationCodeThrottle]  

    def post(self, request):
        email_serializer = EmailSerializer(data=request.data)
        if not email_serializer.is_valid():
            return Response(email_serializer.errors, status=HTTP_400_BAD_REQUEST)

        email = email_serializer.validated_data['email']

        try:
            user = Email.objects.get(email=email).user
        except Email.DoesNotExist:
            raise NotFound({"detail": "User not found."})

        reset_code = PasswordResetCode.objects.filter(user=user).first()
        print(reset_code)

        if reset_code:
            if reset_code.is_valid():
                print("salam")
                return Response({"message": "A valid reset code has already been sent."}, status=HTTP_200_OK)
            else:
                PasswordResetCode.objects.filter(user=user).delete()
                print("salam")

        reset_code, created = PasswordResetCode.objects.get_or_create(user=user)
        # print(reset_code)
        reset_code.generate_code()  
        reset_code.expires_at = timezone.now() + timedelta(minutes=5)
        reset_code.save()  

        send_mail(
            'Password Reset Request',
            f'Hello {user.first_name},\n\nYour password reset code is: {reset_code.code}\nThis code will expire in 5 minutes.',
            'no-reply@yourapp.com',
            [email],
            fail_silently=False,
        )

        return Response({"message": "Password reset code sent."}, status=HTTP_200_OK)

class PasswordResetView(APIView):
    throttle_classes = [SendVerificationCodeThrottle]
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        code = serializer.validated_data['code']
        new_password = serializer.validated_data['new_password']

        try:
            reset_code = PasswordResetCode.objects.get(code=code)
        except PasswordResetCode.DoesNotExist:
            return Response({"detail": "Invalid or expired code."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reset_code.verify_code(code)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user = reset_code.user
        user.set_password(new_password)
        user.save()

        reset_code.delete()

        return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)

