# user_app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserBase, EmailVerificationCode
from WeeklySchedule.models import Teacher
from Grades.models import Student
import logging
from django.utils.timezone import now

logger = logging.getLogger(__name__)

@receiver(post_save, sender=UserBase)
def handle_teacher_creation(sender, instance, created, **kwargs):
    if not created:
        return
    if instance.role and instance.role2 and instance.role2.lower() == 'teacher':
        if not Teacher.objects.filter(national_code=instance.national_code).exists():
            Teacher.objects.create(
                first_name=instance.first_name,
                last_name=instance.last_name,
                national_code=instance.national_code,
                role = instance.role,
                role2=instance.role2,
            )
        elif instance.role2.lower() == 'teacher':
            teacher, created = Teacher.objects.get_or_create(
                national_code=instance.national_code
            )

            teacher.first_name = instance.first_name
            teacher.last_name = instance.last_name
            teacher.role = instance.role
            teacher.role2 = instance.role2
            teacher.save()

@receiver(post_save, sender=EmailVerificationCode)
def cleanup_expired_codes(sender, instance, **kwargs):
    EmailVerificationCode.objects.filter(expires_at__lt=now()).delete()


@receiver(post_save, sender=UserBase)
def create_or_update_student(sender, instance, created, **kwargs):
    if created and instance.role == 'Student':
        Student.objects.create(
            first_name=instance.first_name,
            last_name=instance.last_name,
            national_code=instance.national_code,
            grade=instance.grade,
        )
    elif instance.role == 'Student':
        student, created = Student.objects.get_or_create(
            national_code=instance.national_code
        )

        student.first_name = instance.first_name
        student.last_name = instance.last_name
        student.grade = instance.grade
        student.save()