from django.urls import path
from . import views

urlpatterns = [
    path('analysis/', views.analysis, name="Analysis"),
    path('analysis/text-results/', views.text_analysis_view, name="Text Analysis Results"),
    path('analysis/speech-results/', views.speech_analysis_view, name="Speech Analysis Results"),
]
