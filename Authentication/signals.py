# user_app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserBase, EmailVerificationCode, Student
from WeeklySchedule.models import Teacher
import logging
from django.utils.timezone import now

logger = logging.getLogger(__name__)

@receiver(post_save, sender=UserBase)
def handle_user_creation(sender, instance, created, **kwargs):
    if not created:
        return
    if instance.role and instance.role2 and instance.role2.lower() == 'teacher':
        if not Teacher.objects.filter(name=f"{instance.first_name} {instance.last_name}").exists():
            Teacher.objects.create(name=f"{instance.first_name} {instance.last_name}")
            logger.info(f"Teacher successfully created for user with national_code {instance.national_code}")
    # elif instance.role and instance.role.lower() == 'student':
    #     if not Student.objects.filter(name=f"{instance.first_name} {instance.last_name}").exists():
    #         Student.objects.create(name=f"{instance.first_name} {instance.last_name}")
    #         logger.info(f"Student successfully created for user with national_code {instance.national_code}")
    # else:
        logger.info(f"No action taken for user with national_code {instance.national_code} due to unmatched roles")


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
            role=instance.role,
            role2=instance.role2,
            is_active=instance.is_active,
            is_staff=instance.is_staff
        )
    elif instance.role == 'Student':
        student, created = Student.objects.get_or_create(
            national_code=instance.national_code
        )

        student.first_name = instance.first_name
        student.last_name = instance.last_name
        student.grade = instance.grade
        student.role = instance.role
        student.role2 = instance.role2
        student.is_active = instance.is_active
        student.is_staff = instance.is_staff
        student.save()