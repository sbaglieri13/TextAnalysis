import uuid

from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

import main
import speechRecognition as sr
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


# Webapp views

def homepage(request):
    return render(request, 'homepage.html')


def advanced_analysis(request):
    return render(request, 'advancedAnalysis.html')


# REST POST / homepage.html
@api_view(['POST'])
def results_analysis(request):
    if 'record' in request.POST:
        input_text = sr.record()
        if input_text is None:
            return render(request, 'homepage.html')
    else:
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


# REST POST / advancedAnalysis.html
@api_view(['POST'])
def results_data_analysis(request):
    if 'record' in request.POST:
        input_text = sr.record()
        if input_text is None:
            return render(request, 'advancedAnalysis.html')
    else:
        input_text = request.POST['text']

    input_data = request.FILES['data']
    unique_id = uuid.uuid4()

    text, sentiment, sentiment_acc, sentiment_for_sent, topic, topic_acc, sent_score = main.data_analysis(input_text,
                                                                                                          None,
                                                                                                          input_data)

    sentiment_label_for_sent_str = str(sentiment_for_sent)
    sentiment_label_for_sent_str = sentiment_label_for_sent_str[1:-1]

    table = DataPrediction(
        id=unique_id,
        text=text,
        sentiment=sentiment,
        sentiment_acc=sentiment_acc,
        sentiment_for_sentence=sentiment_label_for_sent_str,
        topic=topic,
        topic_acc=topic_acc
    )
    table.save()

    sentiment_pos = round(sent_score[0], 2)
    sentiment_neu = round(sent_score[1], 2)
    sentiment_neg = round(sent_score[2], 2)

    if topic is None:
        topic = "Topic not found"
        topic_acc = ""
    else:
        topic_acc = str(topic_acc) + " %"

    if sentiment is None:
        sentiment_pos = 0
        sentiment_neu = 0
        sentiment_neg = 0

    context = {'text': text, 'topic': topic, 'topic_acc': topic_acc, 'sentiment_pos': sentiment_pos,
               'sentiment_neu': sentiment_neu, 'sentiment_neg': sentiment_neg, 'sentiment_for_sent': sentiment_for_sent}
    return render(request, 'results.html', context)
