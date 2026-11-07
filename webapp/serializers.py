from pathlib import Path

from rest_framework import serializers

from .models import Analysis

AUDIO_EXTENSIONS = {".wav", ".aif", ".aiff", ".flac"}


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = [
            "id",
            "created_at",
            "source",
            "topic_model",
            "text",
            "sentiment",
            "sentiment_score",
            "sentiment_distribution",
            "sentences",
            "topic",
            "topic_probability",
            "topic_words",
        ]
        read_only_fields = fields


class AnalysisRequestSerializer(serializers.Serializer):
    text = serializers.CharField(required=False, allow_blank=False, max_length=50_000)
    audio = serializers.FileField(required=False)
    corpus = serializers.FileField(required=False)

    def validate_audio(self, value):
        if Path(value.name).suffix.lower() not in AUDIO_EXTENSIONS:
            raise serializers.ValidationError("Upload a WAV, AIFF or FLAC file.")
        return value

    def validate_corpus(self, value):
        if Path(value.name).suffix.lower() != ".txt":
            raise serializers.ValidationError("Upload a .txt file.")
        return value

    def validate(self, attrs):
        if bool(attrs.get("text")) == bool(attrs.get("audio")):
            raise serializers.ValidationError("Provide either 'text' or 'audio'.")
        return attrs
