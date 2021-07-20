from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PredictionTextSerializer, PredictionSpeechSerializer
from .models import PredictionText, PredictionSpeech
import os


# Create your views here.

@api_view(['POST'])
def analysis(request):
    os.system("python main.py " + request.data)
    if " ".join(request.data) == "":
        return HttpResponseRedirect('speech-results/')
    else:
        return HttpResponseRedirect('text-results/')


@api_view(['GET'])
def text_analysis_view(request):
    table = PredictionText.objects.all()
    serializer = PredictionTextSerializer(table, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def speech_analysis_view(request):
    table = PredictionSpeech.objects.all()
    serializer = PredictionSpeechSerializer(table, many=True)
    return Response(serializer.data)
