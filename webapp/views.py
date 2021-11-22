import uuid

from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

import main
from .serializers import PredictionSerializer, DataPredictionSerializer
from .models import Prediction, DataPrediction


@api_view(['POST'])
def text_analysis(request):
    input_text = request.POST['text']
    unique_id = uuid.uuid4()

    text, sentiment, sentiment_acc, topic, topic_acc = main.analysis(input_text, None)

    table = Prediction(
        id=unique_id,
        text=text,
        sentiment=sentiment,
        sentiment_acc=sentiment_acc,
        topic=topic,
        topic_acc=topic_acc
    )
    table.save()

    return HttpResponseRedirect('prediction/' + str(unique_id))


@api_view(['POST'])
def audio_analysis(request):
    audio_data = request.FILES['audio']
    unique_id = uuid.uuid4()

    text, sentiment, sentiment_acc, topic, topic_acc = main.analysis(None, audio_data)

    table = Prediction(
        id=unique_id,
        text=text,
        sentiment=sentiment,
        sentiment_acc=sentiment_acc,
        topic=topic,
        topic_acc=topic_acc
    )
    table.save()

    return HttpResponseRedirect('prediction/' + str(unique_id))


@api_view(['POST'])
def data_text_analysis(request):
    input_text = request.POST['text']
    data = request.FILES['data']
    unique_id = uuid.uuid4()

    text, sentiment, sentiment_acc, sentiment_for_sent, topic, topic_acc = main.data_analysis(input_text, None, data)

    table = DataPrediction(
        id=unique_id,
        text=text,
        sentiment=sentiment,
        sentiment_acc=sentiment_acc,
        sentiment_for_sentence=sentiment_for_sent,
        topic=topic,
        topic_acc=topic_acc
    )
    table.save()

    return HttpResponseRedirect('prediction/' + str(unique_id))


@api_view(['POST'])
def data_audio_analysis(request):
    audio_data = request.FILES['audio']
    data = request.FILES['data']
    unique_id = uuid.uuid4()

    text, sentiment, sentiment_acc, sentiment_for_sent, topic, topic_acc = main.data_analysis(None, audio_data, data)
    table = DataPrediction(
        id=unique_id,
        text=text,
        sentiment=sentiment,
        sentiment_acc=sentiment_acc,
        sentiment_for_sentence=sentiment_for_sent,
        topic=topic,
        topic_acc=topic_acc
    )
    table.save()

    return HttpResponseRedirect('prediction/' + str(unique_id))


@api_view(['GET'])
def analysis_view(request, pk):
    table = Prediction.objects.get(id=pk)
    serializer = PredictionSerializer(table, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def analysis_view_all(request):
    table = Prediction.objects.all()
    serializer = PredictionSerializer(table, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def data_analysis_view(request, pk):
    table = DataPrediction.objects.get(id=pk)
    serializer = DataPredictionSerializer(table, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def data_analysis_view_all(request):
    table = DataPrediction.objects.all()
    serializer = DataPredictionSerializer(table, many=True)
    return Response(serializer.data)


def homepage(request):
    return render(request, 'homepage.html')


def advanced_analysis(request):
    return render(request, 'advancedAnalysis.html')


# REST Post / homepage.html -> input text
@api_view(['POST'])
def results_text_analysis(request):
    input_text = request.POST['text']
    unique_id = uuid.uuid4()

    text, sentiment, sentiment_acc, topic, topic_acc = main.analysis(input_text, None)

    table = Prediction(
        id=unique_id,
        text=text,
        sentiment=sentiment,
        sentiment_acc=sentiment_acc,
        topic=topic,
        topic_acc=topic_acc
    )
    table.save()

    if topic is None:
        topic_label = "Topic not found"
    else:
        topic_label = topic

    if sentiment is None:
        sentiment_label = "Sentiment not found"
    else:
        sentiment_label = sentiment

    context = {'topic': topic_label, 'sentiment': sentiment_label}
    return render(request, 'homepage.html', context)


# REST Post / homepage.html -> input audio
@api_view(['POST'])
def results_audio_analysis(request):
    audio_data = request.FILES['audio']
    unique_id = uuid.uuid4()

    text, sentiment, sentiment_acc, topic, topic_acc = main.analysis(None, audio_data)

    table = Prediction(
        id=unique_id,
        text=text,
        sentiment=sentiment,
        sentiment_acc=sentiment_acc,
        topic=topic,
        topic_acc=topic_acc
    )
    table.save()

    if topic is None:
        topic_label = "Topic not found"
    else:
        topic_label = topic

    if sentiment is None:
        sentiment_label = "Sentiment not found"
    else:
        sentiment_label = sentiment

    context = {'topic': topic_label, 'sentiment': sentiment_label}
    return render(request, 'advancedAnalysis.html', context)
