from rest_framework import serializers
from .models import Absence
from Grades.models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class AbsenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Absence
        fields = ['student', 'date', 'status']  # فیلدهای مورد نیاز برای پاسخ API
        read_only_fields = ['student']  # فقط خواندنی بودن student برای امنیت بیشتر

    def to_representation(self, instance):
        """
        نمایش نام دانش‌آموز به جای شناسه در پاسخ API
        """
        representation = super().to_representation(instance)
        representation['student'] = instance.student.first_name + " " + instance.student.last_name
        representation['grade'] = instance.student.grade
        return representation
