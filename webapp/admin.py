from django.contrib import admin
from .models import PredictionText, PredictionSpeech

# Register your models here.

admin.site.register(PredictionText)
admin.site.register(PredictionSpeech)
