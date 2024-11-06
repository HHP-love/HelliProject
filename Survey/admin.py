from django.contrib import admin

# Register your models here.
from .models import Question, Answer, Choice, Survey
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Choice)
admin.site.register(Survey)