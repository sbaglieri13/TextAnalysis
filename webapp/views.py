import uuid

from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

import main
from .serializers import PredictionSerializer, DataPredictionSerializer
from .models import Prediction, DataPrediction


# Create your views here.


@api_view(['POST'])
def analysis(request):
    input_text = request.POST['text']
    unique_id = uuid.uuid4()
    main.analysis(input_text, unique_id)
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


@api_view(['POST'])
def data_analysis(request):
    input_text = request.POST['text']
    data = request.FILES['data']
    unique_id = uuid.uuid4()
    table = DataPrediction(
        id=unique_id,
        data=data,
    )

    table.save()

    text, sentiment, sentiment_for_sent, topic = main.data_analysis(input_text, data)

    table.text = text
    table.sentiment = sentiment
    table.sentiment_for_sentence = sentiment_for_sent
    table.topic = topic
    table.save()

    return HttpResponseRedirect('prediction/' + str(unique_id))


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