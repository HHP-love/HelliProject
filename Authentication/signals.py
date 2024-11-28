# user_app/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Admin
from WeeklySchedule.models import Teacher
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Admin)
def create_teacher_on_admin_creation(sender, instance, created, **kwargs):
    if created and instance.role and instance.role.lower() == 'teacher':
        Teacher.objects.create(name=f"{instance.first_name} {instance.last_name}")
        logger.info(f"Teacher created for Admin with national_code {instance.national_code}")
    else:
        logger.info(f"Admin with national_code {instance.national_code} did not have role 'Teacher'")

