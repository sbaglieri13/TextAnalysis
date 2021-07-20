from rest_framework import serializers
from .models import PredictionText, PredictionSpeech


class PredictionTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionText
        fields = '__all__'


class PredictionSpeechSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionSpeech
        fields = '__all__'
