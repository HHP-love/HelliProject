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
from django.contrib.auth import authenticate
from .models import Student




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

        # ایجاد توکن و افزودن نقش و کد ملی
        refresh = RefreshToken.for_user(user)
        refresh['role'] = role
        refresh['national_code'] = user.national_code
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': role,
            'national_code': user.national_code,
        }

# serializers.py
from rest_framework import serializers
from .models import Email  

from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


