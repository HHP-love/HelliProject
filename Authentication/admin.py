from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserBase, Email, Student
from django.utils.translation import gettext_lazy as _

# نمایش جزئیات کاربر در لیست admin
class CustomUserAdmin(UserAdmin):
    model = UserBase
    list_display = ('first_name', 'last_name', 'national_code', 'role', 'is_active', 'is_staff', 'grade')
    list_filter = ('role', 'is_active', 'is_staff', 'grade')
    search_fields = ('first_name', 'last_name', 'national_code', 'role')
    ordering = ('national_code',)

    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'national_code', 'role', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Additional Info'), {'fields': ('grade', 'role2')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'national_code', 'password1', 'password2', 'role', 'grade', 'role2')}
        ),
    )

    def save_model(self, request, obj, form, change):
        """
        سفارشی‌سازی برای ذخیره‌سازی کاربر.
        """
        obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

# مدیریت ایمیل‌ها
class EmailAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'is_verified', 'created_at', 'updated_at')
    list_filter = ('is_verified', 'created_at', 'updated_at')
    search_fields = ('user__first_name', 'user__last_name', 'email')
    ordering = ('created_at',)

    def has_delete_permission(self, request, obj=None):
        """
        جلوگیری از حذف ایمیل‌ها از admin.
        """
        return False

# نمایش لیست دانش‌آموزان
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# ثبت مدل‌ها در پنل admin
admin.site.register(UserBase, CustomUserAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(Student, StudentAdmin)
