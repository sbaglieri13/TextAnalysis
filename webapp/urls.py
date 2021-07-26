from django.urls import path
from . import views

urlpatterns = [
    path('analysis/', views.analysis, name="Analysis"),
    path('analysis/prediction/', views.analysis, name="Analysis Results"),
    path('data-analysis/', views.data_analysis, name="Data Analysis"),
    path('data-analysis/prediction/', views.data_analysis, name="Data Analysis Results"),
]
