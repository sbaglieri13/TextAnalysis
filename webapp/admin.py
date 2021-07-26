from django.contrib import admin
from .models import Prediction, DataPrediction

# Register your models here.

admin.site.register(Prediction)
admin.site.register(DataPrediction)
