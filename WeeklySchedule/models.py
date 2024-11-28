from django.db import models

# مدل پایه تحصیلی
class Grade(models.Model):
    grade_choices = [
        ('7', 'هفتم'),
        ('8', 'هشتم'),
        ('9', 'نهم'),
        ('10', 'دهم'),
        ('11', 'یازدهم'),
        ('12', 'دوازدهم'),
    ]
    name = models.CharField(max_length=2, choices=grade_choices, unique=True)

    def __str__(self):
        return self.get_name_display()


# مدل کلاس مدرسه
class SchoolClass(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="classes")
    name = models.CharField(max_length=20) 

    def __str__(self):
        return f"{self.grade} - {self.name}"



class Subject(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name



class Teacher(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name



class Day(models.Model):
    name = models.CharField(max_length=10) 
    order = models.IntegerField(unique=True) 

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']  



# مدل زنگ
class Period(models.Model):
    number = models.IntegerField() 

    def __str__(self):
        return f"زنگ {self.number}"


# مدل برنامه هفتگی
class Schedule(models.Model):
    class_instance = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="schedules")
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name="schedules")
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name="schedules")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="schedules")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="schedules")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['class_instance', 'day', 'period'], name='unique_schedule_for_class_day_period')
        ]

    def __str__(self):
        return f"{self.class_instance} - {self.day} - {self.period} - {self.subject} - {self.teacher}"
