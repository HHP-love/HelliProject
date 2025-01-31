# Generated by Django 5.1.1 on 2024-11-30 19:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Authentication', '0001_initial'),
        ('WeeklySchedule', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GradeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'نوع نمره',
                'verbose_name_plural': 'انواع نمره\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'ترم',
                'verbose_name_plural': 'ترم\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'verbose_name': 'درس',
                'verbose_name_plural': 'دروس',
            },
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('students', models.ManyToManyField(related_name='classrooms', to='Authentication.student')),
                ('teachers', models.ManyToManyField(related_name='classes', to='WeeklySchedule.teacher')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classrooms', to='Grades.semester')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='Grades.subject')),
            ],
            options={
                'verbose_name': 'کلاس',
                'verbose_name_plural': 'کلاس\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('max_score', models.DecimalField(decimal_places=2, default=20, max_digits=5)),
                ('date_recorded', models.DateTimeField(auto_now_add=True)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='Grades.classroom')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='Authentication.student')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='Grades.gradecategory')),
            ],
            options={
                'verbose_name': 'نمره',
                'verbose_name_plural': 'نمرات',
                'constraints': [models.UniqueConstraint(fields=('student', 'classroom', 'category'), name='unique_grade_per_category')],
            },
        ),
    ]
