from django.urls import path
from . import views

urlpatterns = [
    path('audio-analysis/', views.audio_analysis, name="Text Analysis"),
    path('text-analysis/', views.text_analysis, name="Audio Analysis"),
    path('text-analysis/prediction/<str:pk>/', views.analysis_view, name="Text Analysis Results"),
    path('audio-analysis/prediction/<str:pk>/', views.analysis_view, name="Audio Analysis Results"),
    path('analysis/all-prediction/', views.analysis_view_all, name="Analysis Results"),
    path('data-text-analysis/', views.data_text_analysis, name="Text Analysis With Data"),
    path('data-audio-analysis/', views.data_audio_analysis, name="Audio Analysis With Data"),
    path('data-text-analysis/prediction/<str:pk>/', views.data_analysis_view, name="Data Text Analysis Results"),
    path('data-audio-analysis/prediction/<str:pk>/', views.data_analysis_view, name="Data Audio Analysis Results"),
    path('data-analysis/all-prediction/', views.data_analysis_view_all, name="Data Analysis Results"),

    # Link webapp
    path('', views.homepage, name="Homepage"),
    path('advancedAnalysis/', views.advanced_analysis, name="Advanced Analysis"),
    path('results_text_analysis', views.results_text_analysis)
]
