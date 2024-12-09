from django.db import models
from django.core.exceptions import ValidationError
from WeeklySchedule.models import Teacher
from Authentication.models import Student

class Semester(models.Model):
    name = models.CharField(max_length=50) 

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    
    def __str__(self):
        return self.name
    

class Classroom(models.Model):
    name = models.CharField(max_length=100)
    teachers = models.ManyToManyField(Teacher, related_name='classes')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='classes')
    students = models.ManyToManyField(Student, related_name='classrooms')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='classrooms')
    
    def __str__(self):
        return f"{self.name} - {self.subject.name}"


class GradeCategory(models.Model):
    name = models.CharField(max_length=50)  # نام نوع نمره (مثلاً میان‌ترم)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='grades')
    category = models.ForeignKey(GradeCategory, on_delete=models.CASCADE, related_name='grades')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=20)  # نمره‌ی کل برای عنوان
    date_recorded = models.DateTimeField(auto_now_add=True)


    
    class Meta:
        verbose_name = 'نمره'
        verbose_name_plural = 'نمرات'
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'classroom', 'category'], 
                name='unique_grade_per_category'
            )
        ]

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.category.name}: {self.score} / {self.max_score}"

    def clean(self):

        if self.score > self.max_score:
            raise ValidationError("نمره نمی‌تواند بیشتر از نمره کل باشد.")
    def save(self, *args, **kwargs):
        self.clean()  # اجرای متد clean قبل از ذخیره
        super().save(*args, **kwargs)
