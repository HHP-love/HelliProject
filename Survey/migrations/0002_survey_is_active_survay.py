# Generated by Django 5.1.1 on 2024-12-04 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='is_active_survay',
            field=models.BooleanField(default=True),
        ),
    ]
