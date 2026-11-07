import uuid

from django.db import models


class Analysis(models.Model):
    class Source(models.TextChoices):
        TEXT = "text", "Text"
        AUDIO = "audio", "Audio"

    class TopicModel(models.TextChoices):
        PRETRAINED = "pretrained", "Pre-trained (BBC news)"
        CUSTOM_CORPUS = "custom_corpus", "Custom corpus"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=10, choices=Source.choices, default=Source.TEXT)
    topic_model = models.CharField(max_length=20, choices=TopicModel.choices, default=TopicModel.PRETRAINED)
    text = models.TextField()

    sentiment = models.CharField(max_length=10)
    sentiment_score = models.FloatField(help_text="Mean VADER compound score, from -1 to 1.")
    sentiment_distribution = models.JSONField(default=dict, help_text="% of sentences per sentiment label.")
    sentences = models.JSONField(default=list, help_text="Sentiment label and score of every sentence.")

    topic = models.CharField(max_length=255, null=True, blank=True)  # noqa: DJ001
    topic_probability = models.FloatField(null=True, blank=True, help_text="LDA topic probability, from 0 to 1.")
    topic_words = models.JSONField(default=list)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "analyses"

    def __str__(self):
        return f"{self.sentiment} / {self.topic or 'no topic'}: {self.text[:50]}"
