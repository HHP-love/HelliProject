# models.py
from django.db import models
from WeeklySchedule.models import Grade
from django.contrib.auth.hashers import make_password, check_password


class UserBase(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_code = models.CharField(max_length=11, unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=32)

    class Meta:
        abstract = True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"کاربر با کد ملی {self.national_code}"


class Student(UserBase):
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT, related_name='student')


    def __str__(self):
        return f"{self.first_name} {self.last_name} - دانش‌آموز با کد ملی {self.national_code}"


class Admin(UserBase):

    def __str__(self):
        return f"{self.first_name} {self.last_name}  - ادمین با کد ملی {self.national_code}"


class Email(models.Model):
    user = models.OneToOneField(
        'Student', on_delete=models.CASCADE, null=True, blank=True
    )
    admin = models.OneToOneField(
        'Admin', on_delete=models.CASCADE, null=True, blank=True
    )
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # تاریخ ثبت ایمیل
    updated_at = models.DateTimeField(auto_now=True)      # تاریخ آخرین به‌روزرسانی

    def __str__(self):
        return f"ایمیل {self.email} برای {self.user}"