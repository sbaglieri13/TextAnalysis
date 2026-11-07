from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("analyses", views.AnalysisViewSet, basename="analysis")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/health/", views.health, name="health"),
    # Link webapp
    path("", views.homepage, name="homepage"),
    path("results_analysis", views.analyze, name="analyze"),
    path("advancedAnalysis/", views.advanced_analysis, name="advanced-analysis"),
    path("advancedAnalysis/results_data_analysis", views.advanced_results, name="advanced-results"),
]
