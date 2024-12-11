from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from WeeklySchedule.models import Teacher
# from Authentication.models import UserBase



class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_code = models.CharField(max_length=11, unique=True)
    grade = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.full_name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.national_code})"


class Semester(models.Model):
    name = models.CharField(max_length=50, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Classroom(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='classrooms')
    teachers = models.ManyToManyField(Teacher, related_name='classrooms')
    students = models.ManyToManyField(Student, related_name='classrooms')

    def __str__(self):
        return f"{self.name} - {self.subject.name}"


class GradeCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)

    def __str__(self):
        return self.name


class Grade(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('finalized', _('Finalized')),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='grades')
    category = models.ForeignKey(GradeCategory, on_delete=models.CASCADE, related_name='grades')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=20)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
    )
    recorded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    date_recorded = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'classroom', 'category'],
                name='unique_grade_per_category'
            )
        ]

    def clean(self):
        if self.score > self.max_score:
            raise ValidationError(_("The score cannot exceed the maximum score."))

    def __str__(self):
        return f"{self.student.full_name} - {self.category.name}: {self.score}/{self.max_score}"

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class GPA(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='gpa_records')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='gpa_records')
    gpa = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        ordering = ['-gpa'] 
        
    def calculate_weighted_gpa(self):
        total_weighted_score = 0
        total_weights = 0
        
        grades = Grade.objects.filter(student=self.student, classroom__semester=self.semester)
        
        for grade in grades:
            weight = grade.category.weight  # وزن دسته‌بندی نمره
            total_weighted_score += grade.score * weight
            total_weights += weight
        
        if total_weights > 0:
            self.gpa = total_weighted_score / total_weights
        else:
            self.gpa = 0

        self.save()

    def __str__(self):
        return f"{self.student.full_name} - {self.semester.name}: {self.gpa}"



class GradeHistory(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='history')
    old_score = models.DecimalField(max_digits=5, decimal_places=2)
    new_score = models.DecimalField(max_digits=5, decimal_places=2)
    changed_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    change_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Grade Change for {self.grade.student.full_name}: {self.old_score} -> {self.new_score}"



class GradeAppeal(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='appeals')
    reason = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )
    reviewed_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    review_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Appeal for {self.grade} - Status: {self.status}"



class Report(models.Model):
    name = models.CharField(max_length=100)
    generated_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='reports/')

    def __str__(self):
        return f"Report: {self.name} by {self.generated_by}"
