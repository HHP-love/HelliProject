from django.db import models
from Grades.models import Student
# Create your models here.


class Absence(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='absences')  
    grade = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True) 
    date = models.DateField()
    status = models.CharField(default="present", max_length=20)   #presence absence delay

    class Meta:
        unique_together = ('student', 'date') 
        
    def __str__(self):
        return f"{self.student.full_name} در تاریخ {self.date} - {' حاضر بود' if self.status else 'غایب بود'}"