from django.urls import path
from . import views
from .views import ResponseUpdateView

urlpatterns = [
    # مسیر برای لیست کردن و ایجاد نظرسنجی‌ها
    path('surveys/', views.SurveyCreateListView.as_view(), name='survey-list-create'),
    
    # مسیر برای جزئیات، ویرایش و حذف نظرسنجی
    path('surveys/<int:pk>/', views.SurveyDetailView.as_view(), name='survey-detail'),

    # مسیر برای لیست و ایجاد سوالات در نظرسنجی
    path('surveys/<int:survey_id>/questions/', views.QuestionCreateListView.as_view(), name='question-list-create'),
    
    # مسیر برای جزئیات، ویرایش و حذف سوال
    path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name='question-detail'),

    # مسیر برای لیست و ایجاد گزینه‌ها برای سوالات چند گزینه‌ای
    path('questions/<int:question_id>/choices/', views.ChoiceCreateListView.as_view(), name='choice-list-create'),
    
    # مسیر برای جزئیات، ویرایش و حذف گزینه
    path('choices/<int:pk>/', views.ChoiceDetailView.as_view(), name='choice-detail'),

    # مسیر برای ثبت پاسخ کاربر به سوالات
    path('responses/', views.ResponseCreateView.as_view(), name='response-create'),

    path('responses/<int:pk>/edit/', ResponseUpdateView.as_view(), name='edit-response'),
]
