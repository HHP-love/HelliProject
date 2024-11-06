from rest_framework import generics
from datetime import datetime
from .models import Survey, Question, Choice, Answer, Student
from rest_framework.exceptions import ValidationError
from .serializers import SurveySerializer, QuestionSerializer, ChoiceSerializer, ResponseSerializer, AnswerSerializer
from drf_spectacular.utils import extend_schema
from django.http import HttpRequest

# ویو برای لیست کردن و ایجاد نظرسنجی
class SurveyCreateListView(generics.ListCreateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    @extend_schema(summary="لیست نظرسنجی‌ها")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="ایجاد نظرسنجی جدید")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# ویو برای جزئیات، ویرایش و حذف نظرسنجی
class SurveyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    @extend_schema(summary="دریافت جزئیات نظرسنجی")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# ویو برای لیست و ایجاد سوالات
class QuestionCreateListView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        survey_id = self.kwargs['survey_id']
        return Question.objects.filter(survey_id=survey_id)

    @extend_schema(summary="لیست سوالات نظرسنجی")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="ایجاد سوال جدید")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# ویو برای جزئیات، ویرایش و حذف سوال
class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @extend_schema(summary="دریافت جزئیات سوال")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# ویو برای لیست و ایجاد گزینه‌های سوالات چند گزینه‌ای
class ChoiceCreateListView(generics.ListCreateAPIView):
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        question_id = self.kwargs['question_id']
        return Choice.objects.filter(question_id=question_id)

    @extend_schema(summary="لیست گزینه‌ها")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="ایجاد گزینه جدید")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# ویو برای جزئیات، ویرایش و حذف گزینه
class ChoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    @extend_schema(summary="دریافت جزئیات گزینه")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# ویو برای ثبت پاسخ کاربر به سوالات
class ResponseCreateView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = ResponseSerializer

    @extend_schema(summary="ثبت پاسخ به سوال")
    def post(self, request: HttpRequest, *args, **kwargs):
        user_ip = request.META.get('REMOTE_ADDR')
        if Answer.objects.filter(ip_address=user_ip).exists():
            raise ValidationError("این IP قبلاً پاسخ داده است.")
        # استخراج کد ملی از داده‌های درخواست
        national_code = request.data.get('national_code')

        if not national_code:
            raise ValidationError("کد ملی الزامی است.")

        # پیدا کردن کاربر بر اساس کد ملی
        user = Student.objects.filter(national_code=national_code).first()

        if not user:
            raise ValidationError("کاربر با این کد ملی پیدا نشد.")

        data = request.data.copy()  # کپی داده‌ها
        data['user'] = user.id  # اضافه کردن شناسه کاربر به داده‌ها

        # اعتبارسنجی سوال و پاسخ
        question_id = data.get('question')
        question = Question.objects.filter(id=question_id).first()

        if question:
            if question.question_type == Question.TEXT and not data.get('answer_text'):
                raise ValidationError("پاسخ متنی الزامی است برای سوالات متنی.")
            if question.question_type == Question.MULTIPLE_CHOICE and not data.get('choice'):
                raise ValidationError("انتخاب گزینه الزامی است برای سوالات چند گزینه‌ای.")
            
        # بررسی تاریخ پایان نظرسنجی
        survey = question.survey  # نظرسنجی مربوطه به سوال
        current_date = datetime.now()

        if current_date > survey.end_date:
            raise ValidationError("زمان ثبت نظر برای این نظرسنجی به پایان رسیده است.")

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    








class ResponseUpdateView(generics.UpdateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
 # فقط کاربران وارد شده می‌توانند پاسخ خود را ویرایش کنند

    def get_object(self):
        # گرفتن شیء پاسخ از دیتابیس
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("شما مجاز به ویرایش این پاسخ نیستید.")  # کاربر نمی‌تواند پاسخ دیگران را ویرایش کند

        # بررسی وضعیت فعال بودن نظرسنجی
        survey = obj.survey
        if not survey.is_active():
            raise ValidationError("این نظرسنجی به پایان رسیده است. پاسخ‌ها قابل ویرایش نیستند.")

        return obj

    def update(self, request, *args, **kwargs):
        # بررسی ویرایش کردن پاسخ
        return super().update(request, *args, **kwargs)

    @extend_schema(summary="ویرایش پاسخ به سوال")
    def patch(self, request, *args, **kwargs):
        # برای ویرایش از متد PATCH استفاده می‌کنیم
        return super().patch(request, *args, **kwargs)