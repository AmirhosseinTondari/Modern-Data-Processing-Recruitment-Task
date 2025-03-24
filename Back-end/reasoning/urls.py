from django.urls import path
from . import views

urlpatterns = [
    path('cot/', views.CoTView.as_view()),
    path('cotsc/', views.CoTSCView.as_view()),
    path('history/', views.HistoryView.as_view()),
]