import uuid

from django.db import models


# Create your models here.

class Prediction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    text = models.TextField()
    sentiment = models.CharField(max_length=255, null=True)
    sentiment_acc = models.FloatField(null=True)
    topic = models.CharField(max_length=255, null=True)
    topic_acc = models.FloatField(null=True)

    def __str__(self):
        return self.text


class DataPrediction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    text = models.TextField()
    sentiment = models.TextField(null=True)
    sentiment_acc = models.FloatField(null=True)
    sentiment_for_sentence = models.TextField(null=True)
    topic = models.TextField(null=True)
    topic_acc = models.FloatField(null=True)

    def __str__(self):
        return self.text
