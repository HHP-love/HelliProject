from django.db import models
from Authentication.models import Student
from django.core.exceptions import ValidationError
from django.utils import timezone

# مدل نظرسنجی
class Survey(models.Model):
    title = models.CharField(max_length=255)  # عنوان نظرسنجی
    description = models.TextField()  # توضیحات نظرسنجی
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()  # تاریخ شروع
    end_date = models.DateTimeField()  # تاریخ پایان

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError("تاریخ پایان باید بعد از تاریخ شروع باشد.")
    def is_active(self):
        return self.start_date <= timezone.now() <= self.end_date


    def __str__(self):
        return self.title


# مدل سوال
class Question(models.Model):
    TEXT = 'text'
    MULTIPLE_CHOICE = 'multiple_choice'

    QUESTION_TYPES = [
        (TEXT, 'متنی'),
        (MULTIPLE_CHOICE, 'چند گزینه‌ای'),
    ]

    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)  # هر سوال متعلق به یک نظرسنجی است
    question_text = models.CharField(max_length=500)  # متن سوال
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES, default=TEXT)  # نوع سوال

    def __str__(self):
        return self.question_text


# مدل گزینه برای سوال‌های چند گزینه‌ای
class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)  # هر گزینه متعلق به یک سوال است
    choice_text = models.CharField(max_length=255)  # متن گزینه

    def __str__(self):
        return self.choice_text


# مدل ثبت پاسخ‌های کاربر
class Answer(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)  # کاربری که پاسخ داده
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # سوال مربوطه
    answer_text = models.TextField(blank=True, null=True)  # پاسخ کاربر (برای سوالات متنی)
    choice = models.ForeignKey(Choice, blank=True, null=True, on_delete=models.CASCADE)  # گزینه انتخاب شده برای سوال‌های چند گزینه‌ای
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # زمان ویرایش آخرین پاسخ
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')  # جلوگیری از پاسخ تکراری برای هر کاربر در یک سوال

    def clean(self):
        if self.question.question_type == Question.TEXT and not self.answer_text:
            raise ValidationError("پاسخ متنی الزامی است برای سوالات متنی.")
        if self.question.question_type == Question.MULTIPLE_CHOICE and not self.choice:
            raise ValidationError("انتخاب گزینه الزامی است برای سوالات چند گزینه‌ای.")

    def __str__(self):
        return f"{self.user.national_code} - {self.question.question_text}"
