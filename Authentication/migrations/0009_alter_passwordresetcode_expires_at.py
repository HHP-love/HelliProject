# Generated by Django 5.1.1 on 2025-02-24 15:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0008_remove_userbase_class_in_grade_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetcode',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 24, 15, 24, 51, 619912, tzinfo=datetime.timezone.utc)),
        ),
    ]
