from django.db import models


# Create your models here.

class Prediction(models.Model):
    text = models.TextField()
    sentiment = models.CharField(max_length=10, null=True)
    sentiment_acc = models.FloatField(null=True)
    topic = models.CharField(max_length=20, null=True)
    topic_acc = models.FloatField(null=True)

    def __str__(self):
        return '__all__'


class DataPrediction(models.Model):
    text = models.TextField()
    data = models.FileField(upload_to='data')
    sentiment = models.TextField(null=True)
    sentiment_for_sentence = models.TextField(null=True)
    topic = models.TextField(null=True)

    def __str__(self):
        return '__all__'
