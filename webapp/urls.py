from django.urls import path
from . import views

urlpatterns = [
    path('analysis/', views.analysis, name="Analysis"),
    path('analysis/prediction/<str:pk>/', views.analysis_view, name="Analysis Results"),
    path('analysis/all-prediction/', views.analysis_view_all, name="Analysis Results"),
    path('data-analysis/', views.data_analysis, name="Data Analysis"),
    path('data-analysis/prediction/<str:pk>/', views.data_analysis_view, name="Data Analysis"),
    path('data-analysis/all-prediction/', views.data_analysis_view_all, name="Data Analysis Results"),
]
