# user_app/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import UserBase, Student
from WeeklySchedule.models import Teacher
import logging

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

