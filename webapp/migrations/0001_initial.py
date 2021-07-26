# Generated by Django 3.2.5 on 2021-07-26 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataPrediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('data', models.FileField(upload_to='data')),
                ('sentiment', models.TextField(null=True)),
                ('sentiment_for_sentence', models.TextField(null=True)),
                ('topic', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('sentiment', models.CharField(max_length=10, null=True)),
                ('sentiment_acc', models.FloatField(null=True)),
                ('topic', models.CharField(max_length=20, null=True)),
                ('topic_acc', models.FloatField(null=True)),
            ],
        ),
    ]
