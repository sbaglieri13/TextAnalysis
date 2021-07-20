from django.db import models


# Create your models here.

class PredictionText(models.Model):
    text = models.TextField(unique=True)
    sentiment = models.CharField(max_length=10, null=True)
    sentiment_acc = models.FloatField(null=True)
    topic = models.CharField(max_length=20, null=True)
    topic_acc = models.FloatField(null=True)

    def __str__(self):
        return '__all__'


class PredictionSpeech(models.Model):
    speech_text = models.TextField(unique=True)
    sentiment = models.CharField(max_length=10, null=True)
    sentiment_acc = models.FloatField(null=True)
    topic = models.CharField(max_length=20, null=True)
    topic_acc = models.FloatField(null=True)

    def __str__(self):
        return '__all__'
