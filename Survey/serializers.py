from rest_framework import serializers
from .models import Survey, Question, Choice, Answer

# Serializer برای مدیریت نظرسنجی‌ها
class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'start_date', 'end_date']

# Serializer برای مدیریت سوالات
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'survey', 'question_text', 'question_type']

# Serializer برای مدیریت گزینه‌های سوالات چند گزینه‌ای
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'question', 'choice_text']

# Serializer برای مدیریت پاسخ‌های کاربران به سوالات
class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'user', 'question', 'answer_text']

    def validate(self, attrs):
        question = attrs.get('question')
        if question:
            if question.question_type == Question.TEXT and not attrs.get('answer_text'):
                raise serializers.ValidationError("پاسخ متنی الزامی است.")
            elif question.question_type == Question.MULTIPLE_CHOICE and not attrs.get('choice'):
                raise serializers.ValidationError("انتخاب گزینه الزامی است.")
        return attrs


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id',  'user', 'answer_text', 'choice', 'updated_at', 'created_at']
        read_only_fields = ['user', 'survey', 'created_at']
