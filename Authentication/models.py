from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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
        return self.create_user(national_code, password, role='Admin', **extra_fields)

class UserBase(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_code = models.CharField(max_length=11, unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(
        max_length=32,
        choices=[('Student', 'Student'), ('Admin', 'Admin')],
        default='Student'
    )
    grade = models.ForeignKey(
        'WeeklySchedule.Grade',
        on_delete=models.PROTECT,
        related_name='students',
        null=True,
        blank=True
    )
    role2 = models.CharField(max_length=32, null= True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'national_code'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role} ({self.national_code})"


class Student(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name})"


from django.db import models
from django.conf import settings


class Email(models.Model):
    """
    مدل ایمیل برای مدیریت ایمیل‌های کاربران.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # ارجاع به مدل کاربر سفارشی
        on_delete=models.CASCADE,
        related_name='email_info'  # دسترسی به ایمیل کاربر از طریق user.email_info
    )
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # تاریخ ثبت ایمیل
    updated_at = models.DateTimeField(auto_now=True)      # تاریخ آخرین به‌روزرسانی

    def __str__(self):
        return f"ایمیل {self.email} برای {self.user}"
