# Generated by Django 5.1.3 on 2024-11-06 18:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('order', models.IntegerField(unique=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('7', 'هفتم'), ('8', 'هشتم'), ('9', 'نهم'), ('10', 'دهم'), ('11', 'یازدهم'), ('12', 'دوازدهم')], max_length=2, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='WeeklySchedule.grade')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='WeeklySchedule.day')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='WeeklySchedule.period')),
                ('class_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='WeeklySchedule.schoolclass')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='WeeklySchedule.subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='WeeklySchedule.teacher')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('class_instance', 'day', 'period'), name='unique_schedule_for_class_day_period')],
            },
        ),
    ]