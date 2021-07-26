from rest_framework import serializers
from .models import Prediction, DataPrediction


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'


class DataPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPrediction
        fields = '__all__'
