from rest_framework import serializers
from .models import Prediction, DataPrediction


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ['id', 'text', 'sentiment', 'sentiment_acc', 'topic', 'topic_acc']


class DataPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPrediction
        fields = ['id', 'text', 'data', 'sentiment', 'sentiment_for_sentence', 'topic']
