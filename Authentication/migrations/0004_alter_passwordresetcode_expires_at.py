# Generated by Django 5.1.1 on 2025-02-02 20:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0003_alter_passwordresetcode_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetcode',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 2, 20, 18, 6, 650771, tzinfo=datetime.timezone.utc)),
        ),
    ]
