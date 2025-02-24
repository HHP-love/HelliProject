from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from Grades.models import Student

class CustomUserManager(BaseUserManager):
    def create_user(self, national_code, password=None, role='Student', **extra_fields):
        if not national_code:
            raise ValueError("The National Code must be set.")
        if role not in ['Student', 'Admin']:
            raise ValueError("Invalid role specified.")

        user = self.model(national_code=national_code, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, national_code, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(national_code, password, **extra_fields)

class UserBase(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
            ('student', 'student'),
            ('parent', 'parent'),
            ('teacher', 'teacher'),
            ('assistant', 'assistant'),
            ('principal', 'principal'),
        ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_code = models.CharField(max_length=11, unique=True)
    password = models.CharField(max_length=128)
    grade = models.ForeignKey(
        'WeeklySchedule.Grade',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='users'
    )
    role = models.CharField(
        max_length=32,
        choices=[('Student', 'Student'), ('Admin', 'Admin'), ('Parent', 'Parent')],
        default='Student'
    )
    role2 = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'national_code'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role} ({self.national_code})"




from django.conf import settings

class Email(models.Model):
    """
    مدل ایمیل برای مدیریت ایمیل‌های کاربران.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='email_info'
    )
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)      

    def __str__(self):
        return f"Email: ({self.email}) for {self.user}   and is_verified : {self.is_verified}"



from hashlib import sha256
from django.utils.timezone import now

class EmailVerificationCode(models.Model):
    mail = models.ForeignKey(Email, on_delete=models.CASCADE, related_name='verification_codes')
    code = models.CharField(max_length=64)  # Hashed
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.IntegerField(default=0)

    def set_code(self, raw_code):
        self.code = sha256(raw_code.encode()).hexdigest()

    def verify_code(self, raw_code):
        return self.code == sha256(raw_code.encode()).hexdigest()

    def is_valid(self):
        return now() < self.expires_at




import random
import string
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

class PasswordResetCode(models.Model):
    user = models.ForeignKey(UserBase, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(minutes=5))
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_code(self):
        self.code = ''.join(random.choices(string.digits, k=6))
        # self.expires_at = timezone.now() + timedelta(minutes=5)
        self.attempts = 0
        self.save()

    def is_valid(self):
        if timezone.now() > self.expires_at:
            # raise ValidationError("Code expired.")
            return False
        return True

    def verify_code(self, input_code):
        if self.attempts >= 3:
            raise ValidationError("Too many failed attempts.")
        if self.code != input_code:
            self.attempts += 1
            self.save()
            raise ValidationError("Invalid code.")
        self.is_valid()
        return True


class Parent(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_code = models.CharField(max_length=11, unique=True)
    students = models.ManyToManyField(Student, related_name='parents')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.national_code})"








from django.conf import settings

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)  # نام نقش
    description = models.TextField(blank=True, null=True)  # توضیحات نقش
    permissions = models.ManyToManyField('Permission', blank=True)  # ارتباط با دسترسی‌ها

    def __str__(self):
        return self.name


class Permission(models.Model):
    name = models.CharField(max_length=50, unique=True)  
    codename = models.CharField(max_length=50, unique=True)  
    description = models.TextField(blank=True, null=True)  

    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users')
    assigned_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.user} - {self.role}"