# serializers.py
from rest_framework import serializers
from .models import *

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'national_code', 'grade']  

    def validate_slug(self, value):
        if Student.objects.filter(slug=value).exists():
            raise serializers.ValidationError("Student with this slug already exists.")
        return value

    def validate(self, data):
        return data



from rest_framework import serializers
from .models import Semester

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'name', 'start_date', 'end_date']

    # def validate_name(self, value):
    #     if Semester.objects.filter(name=value).exists():
    #         raise serializers.ValidationError("Semester with this name already exists.")
    #     return value

    def validate(self, data):
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return data




class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'slug']




class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'last_name']    #TODO 123



class ClassroomSerializer(serializers.ModelSerializer):
    teachers = TeacherSerializer(many=True, read_only=True)
    students = StudentSerializer(many=True, read_only=True)
    subject = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ['id', 'name', 'subject', 'teachers', 'students']


# class ClassroomSerializer(serializers.ModelSerializer):
#     teachers = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), many=True)
#     students = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)
#     subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())

#     class Meta:
#         model = Classroom
#         fields = ['id', 'name', 'subject', 'teachers', 'students']

class ClassroomCreateUpdateSerializer(serializers.ModelSerializer):
    subjects = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), many=True)
    teachers = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), many=True)
    students = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)

    class Meta:
        model = Classroom
        fields = ['name', 'subjects', 'teachers', 'students']



from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['student', 'classroom', 'category', 'score', 'max_score']

    def validate_score(self, value):
        """
        اعتبارسنجی نمره وارد شده. اطمینان حاصل می‌کنیم که نمره بیشتر از نمره حداکثر نباشد.
        """
        max_score = self.initial_data.get('max_score')
        if value > float(max_score):
            raise ValidationError(_("The score cannot exceed the maximum score."))
        return value

    # def create(self, validated_data):
    #     """
    #     هنگام ایجاد نمره، معلم (recorded_by) را به صورت خودکار اضافه می‌کنیم.
    #     """
    #     validated_data['recorded_by'] = self.context['request'].user
    #     return super().create(validated_data)


class GradeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['score', 'category']


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['student', 'classroom', 'category', 'score', 'date_assigned']


class GPASerializer(serializers.ModelSerializer):
    calculated_gpa = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)

    class Meta:
        model = GPA
        fields = ['student', 'semester', 'gpa', 'calculated_gpa']

class CompareGPASerializer(serializers.Serializer):
    semester = serializers.CharField()
    gpa = serializers.DecimalField(max_digits=4, decimal_places=2)

class GPAListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPA
        fields = ['student', 'semester', 'gpa', 'calculated_gpa']

class GPAHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GPAHistory
        fields = ['gpa_record', 'old_gpa', 'new_gpa', 'changed_by', 'change_date']