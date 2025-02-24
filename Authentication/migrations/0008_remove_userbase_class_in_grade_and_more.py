# Generated by Django 5.1.1 on 2025-02-24 15:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0007_alter_passwordresetcode_expires_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userbase',
            name='class_in_grade',
        ),
        migrations.AlterField(
            model_name='passwordresetcode',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 24, 15, 22, 1, 40170, tzinfo=datetime.timezone.utc)),
        ),
    ]
