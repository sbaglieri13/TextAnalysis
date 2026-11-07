from django.contrib import admin

from .models import Analysis


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ("created_at", "source", "topic_model", "sentiment", "sentiment_score", "topic", "topic_probability")
    list_filter = ("source", "topic_model", "sentiment")
    search_fields = ("text", "topic")
    readonly_fields = [field.name for field in Analysis._meta.fields]
