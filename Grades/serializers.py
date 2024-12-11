# serializers.py
from rest_framework import serializers
from .models import *

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'national_code', 'grade']

    def validate_national_code(self, value):
        # Validation for national code (for example, check length)
        if len(value) != 11:
            raise serializers.ValidationError("National code must be 11 characters.")
        return value

    def validate(self, data):
        # Custom validation logic can go here
        if Student.objects.filter(national_code=data['national_code']).exists():
            raise serializers.ValidationError("Student with this national code already exists.")
        return data



class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'name', 'start_date', 'end_date']



class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code']
