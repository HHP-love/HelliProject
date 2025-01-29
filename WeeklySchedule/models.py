from django.db import models


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



class SchoolClass(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="classes")
    name = models.CharField(max_length=20) 
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.grade} - {self.name}")  # Slugify the class name with the grade
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.grade} - {self.name}"



class Subject(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Slugify the subject name
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name


from django.utils.text import slugify
class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    national_code = models.CharField(max_length=11, unique=True)
    role = models.CharField(max_length=32)
    role2 = models.CharField(max_length=32, null= True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __post_init__(self):
        self.full_name = f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name} {self.last_name}")  # Slugify the full name
            self.full_name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_name_display()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.national_code})"



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
