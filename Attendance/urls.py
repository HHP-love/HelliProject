from django.urls import path
from .views import AbsenceListView, AbsenceDetailView, RecordAbsenceView

urlpatterns = [
    path('', AbsenceListView.as_view(), name='absence-list'),
    path('create/', RecordAbsenceView.as_view(), name='absence-list'),
    path('detail/<str:national_code>/<str:date>/', AbsenceDetailView.as_view(), name='detail-absence'),

]