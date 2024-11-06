# serializers.py

from rest_framework import serializers
from .models import Grade, SchoolClass, Subject, Teacher, Day, Period, Schedule


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


class SchoolClassSerializer(serializers.ModelSerializer):
    grade = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all())

    class Meta:
        model = SchoolClass
        fields = ['id', 'name', 'grade']  


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'



class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'



class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = '__all__'



class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'





# class ScheduleSerializer(serializers.ModelSerializer):
#     class_instance = serializers.PrimaryKeyRelatedField(queryset=SchoolClass.objects.all())
#     day = serializers.PrimaryKeyRelatedField(queryset=Day.objects.all())
#     period = serializers.PrimaryKeyRelatedField(queryset=Period.objects.all())
#     subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
#     teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
#     def create(self, validated_data):
#         # اینجا ما از داده‌های تأیید شده استفاده می‌کنیم و ارتباط‌ها را به درستی ایجاد می‌کنیم
#         return Schedule.objects.create(**validated_data)
#     class Meta:
#         model = Schedule
#         fields = ['id', 'class_instance', 'day', 'period', 'subject', 'teacher']


# class ScheduleSerializer(serializers.ModelSerializer):
#     class_instance = serializers.CharField(source='class_instance.name')
#     day = serializers.CharField(source='day.name')
#     period = serializers.CharField(source='period.number')
#     subject = serializers.CharField(source='subject.name')
#     teacher = serializers.CharField(source='teacher.name')

#     class Meta:
#         model = Schedule
#         fields = ['id', 'class_instance', 'day', 'period', 'subject', 'teacher']


# from rest_framework import serializers
# from .models import Schedule, SchoolClass, Day, Period, Subject, Teacher

# class ScheduleSerializer(serializers.ModelSerializer):
#     class_instance = serializers.StringRelatedField()
#     day = serializers.StringRelatedField()
#     period = serializers.StringRelatedField()
#     subject = serializers.StringRelatedField()
#     teacher = serializers.StringRelatedField()

#     class Meta:
#         model = Schedule
#         fields = ['id', 'class_instance', 'day', 'period', 'subject', 'teacher']

#     def create(self, validated_data):
#         # ساخت شی جدید با داده‌های ورودی
#         return Schedule.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         # به‌روزرسانی شی موجود
#         instance.class_instance = validated_data.get('class_instance', instance.class_instance)
#         instance.day = validated_data.get('day', instance.day)
#         instance.period = validated_data.get('period', instance.period)
#         instance.subject = validated_data.get('subject', instance.subject)
#         instance.teacher = validated_data.get('teacher', instance.teacher)
#         instance.save()
#         return instance


class ScheduleSerializer(serializers.ModelSerializer):
    class_instance = serializers.PrimaryKeyRelatedField(queryset=SchoolClass.objects.all())
    day = serializers.PrimaryKeyRelatedField(queryset=Day.objects.all())
    period = serializers.PrimaryKeyRelatedField(queryset=Period.objects.all())
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())

    # این فیلدها برای بازگشت نام‌ها به‌جای id
    class_instance_name = serializers.StringRelatedField(source='class_instance')
    day_name = serializers.StringRelatedField(source='day')
    period_name = serializers.StringRelatedField(source='period')
    subject_name = serializers.StringRelatedField(source='subject')
    teacher_name = serializers.StringRelatedField(source='teacher')

    class Meta:
        model = Schedule
        fields = ['id', 'class_instance', 'day', 'period', 'subject', 'teacher', 
                  'class_instance_name', 'day_name', 'period_name', 'subject_name', 'teacher_name']

    def create(self, validated_data):
        return Schedule.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.class_instance = validated_data.get('class_instance', instance.class_instance)
        instance.day = validated_data.get('day', instance.day)
        instance.period = validated_data.get('period', instance.period)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.teacher = validated_data.get('teacher', instance.teacher)
        instance.save()
        return instance




