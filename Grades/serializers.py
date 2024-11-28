from rest_framework import serializers
from .models import Teacher, Student, Classroom, Grade, GradeCategory

class TeacherSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='name', read_only=True)  
    classes = serializers.PrimaryKeyRelatedField(many=True, read_only=True) 

    class Meta:
        model = Teacher
        fields = ['full_name', 'classes']


class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='name', read_only=True)
    classrooms = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  

    class Meta:
        model = Student
        fields = ['full_name', 'classrooms']


class ClassroomSerializer(serializers.ModelSerializer):
    teachers = TeacherSerializer(many=True, read_only=True)
    students = StudentSerializer(many=True, read_only=True)
    subject = serializers.CharField(source='subject.name')  # نام درس به جای شناسه

    class Meta:
        model = Classroom
        fields = ['name', 'teachers', 'students', 'subject', 'semester']


class GradeSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    classroom = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all())
    grade_category = serializers.CharField(source='GradeCategory.name', read_only=True)

    class Meta:
        model = Grade
        fields = ['student', 'classroom', 'grade_category', 'score', 'date']


