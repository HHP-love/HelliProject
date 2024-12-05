# serializers.py


from rest_framework import serializers
from .models import Student,UserBase
from WeeklySchedule.models import Grade

class StudentSignupSerializer(serializers.ModelSerializer):
    grade = serializers.CharField(write_only=True)

    class Meta:
        model = UserBase
        fields = ['first_name', 'last_name', 'national_code', 'password', 'grade', 'role']

    def create(self, validated_data):
        # پیدا کردن Grade از طریق name
        grade_name = validated_data.pop('grade')
        try:
            grade = Grade.objects.get(name=grade_name)
        except Grade.DoesNotExist:
            raise serializers.ValidationError({"grade": "کلاسی با این نام یافت نشد."})

        student = UserBase(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            national_code=validated_data['national_code'],
            grade=grade,  # ارتباط با Grade
            role=validated_data['role']
        )
        student.set_password(validated_data['password'])
        student.save()
        return student

    def validate_national_code(self, value):
        """اعتبارسنجی برای کد ملی که 10 رقم باشد"""
        if len(value) != 10:
            raise serializers.ValidationError("کد ملی باید 10 رقم باشد.")
        return value




class AdminSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBase
        fields = ['first_name', 'last_name','national_code', 'password', 'role', 'role2']

    def create(self, validated_data):
        admin = UserBase(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            national_code=validated_data['national_code'],
            role = validated_data['role'],
            role2 = validated_data['role2']
        )
        admin.set_password(validated_data['password'])
        admin.save()
        return admin


from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

class LoginSerializer(serializers.Serializer):
    national_code = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        national_code = data.get("national_code")
        password = data.get("password")
        
        # جستجو برای دانش‌آموز یا ادمین
        user = None
        role = None
        try:
            user = UserBase.objects.get(national_code=national_code)
            role = 'student' if user.role == 'Student' else 'admin'
        except UserBase.DoesNotExist:
            raise serializers.ValidationError("کاربری با این کد ملی یافت نشد.")


        # بررسی رمز عبور
        if not user.check_password(password):
            raise serializers.ValidationError("رمز عبور اشتباه است.")
        
        # اضافه کردن نقش به داده‌ها
        data['user'] = user
        data['role'] = role

        return data

    def create(self, validated_data):
        user = validated_data.get('user')
        role = validated_data.get('role')


        refresh = RefreshToken.for_user(user)
        refresh['role'] = role
        refresh['national_code'] = user.national_code
        refresh['name'] = user.first_name + " " + user.last_name,
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': role,
            'national_code': user.national_code,
            'name' : user.first_name + " " + user.last_name,
        }
        
        # response = JsonResponse({
        #     'refresh': str(refresh),
        #     'access': str(refresh.access_token),
        #     'role': role,
        #     'national_code': user.national_code,
        #     'name': user.first_name + " " + user.last_name,
        # })

        # # ارسال توکن Refresh در کوکی
        # response.set_cookie(
        #     'refresh_token', str(refresh), 
        #     httponly=True, secure=True, samesite='Strict'
        # )
        # response.set_cookie(
        #     'access_token', str(refresh), 
        #     httponly=True, secure=True, samesite='Strict'
        # )

        # # ارسال توکن Access در هدر Authorization
        # response['Authorization'] = f"Bearer {str(refresh.access_token)}"
        
        # return response




class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()



class SendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email field is required.")
        return value
    


class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)

    def validate_code(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Invalid verification code.")
        return value


