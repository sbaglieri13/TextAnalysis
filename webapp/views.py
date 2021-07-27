from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

import main
from .serializers import PredictionSerializer, DataPredictionSerializer
from .models import Prediction, DataPrediction


# Create your views here.


@api_view(['GET', 'POST'])
def analysis(request):
    if request.method == 'POST':
        input_text = request.POST['text']
        main.analysis(input_text)
        return HttpResponseRedirect('prediction/')
    elif request.method == 'GET':
        table = Prediction.objects.all()
        serializer = PredictionSerializer(table, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def data_analysis(request):
    if request.method == 'POST':
        input_text = request.POST['text']
        data = request.FILES['data']

        table = DataPrediction(
            data=data,
        )

        table.save()

        text, sentiment, sentiment_for_sent, topic = main.data_analysis(input_text, data)

        table.text = text
        table.sentiment = sentiment
        table.sentiment_for_sentence = sentiment_for_sent
        table.topic = topic
        table.save()

        return HttpResponseRedirect('prediction/')

    elif request.method == 'GET':
        table = DataPrediction.objects.all()
        serializer = DataPredictionSerializer(table, many=True)
        return Response(serializer.data)
