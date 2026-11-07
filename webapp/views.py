from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from nlp.topics import TopicModelNotTrainedError

from .models import Analysis
from .serializers import AUDIO_EXTENSIONS, AnalysisRequestSerializer, AnalysisSerializer
from .services import AnalysisError, run_analysis


class AnalysisViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def create(self, request):
        request_data = AnalysisRequestSerializer(data=request.data)
        request_data.is_valid(raise_exception=True)
        try:
            analysis = run_analysis(**request_data.validated_data)
        except TopicModelNotTrainedError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except AnalysisError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(AnalysisSerializer(analysis).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})


# Webapp views

THEMES = {
    "Arts, Culture & Entertainment": ("Arts", "arts-and-culture"),
    "Nature - Environment": ("Nature", "nature"),
    "Environmental issue & Environmental pollution": ("Nature", "nature"),
    "News & Politics": ("News", "news"),
}
TENSE_MUSIC = {"arts-and-culture", "nature"}


def stage_scene(topic: str | None, sentiment: str) -> dict | None:
    if topic not in THEMES:
        return None
    theme, music = THEMES[topic]
    mood = sentiment.capitalize()
    if sentiment == "NEGATIVE" and music in TENSE_MUSIC:
        music += "-tense"
    return {
        "css": f"webapp/css/topicStyle/styleTopic{theme}{mood}.css",
        "audio": f"webapp/audio/{music}.m4a",
    }


def _uploaded(request, name: str):
    file = request.FILES.get(name)
    return file if file and file.size else None


def _form_input(request) -> dict:
    audio = _uploaded(request, "audio")
    if audio is not None:
        if not audio.name.lower().endswith(tuple(AUDIO_EXTENSIONS)):
            raise ValueError("Upload a WAV, AIFF or FLAC audio file.")
        return {"audio": audio}
    text = request.POST.get("text", "").strip()
    if not text:
        raise ValueError("Write some text or record an audio clip first.")
    return {"text": text}


@require_GET
def homepage(request):
    return render(request, "homepage.html")


@require_GET
def advanced_analysis(request):
    return render(request, "advancedAnalysis.html")


# REST POST / homepage.html
@require_http_methods(["POST"])
def analyze(request):
    try:
        analysis = run_analysis(**_form_input(request))
    except (ValueError, *AnalysisError) as exc:
        return render(request, "homepage.html", {"error": str(exc)}, status=400)
    context = {"analysis": analysis, "scene": stage_scene(analysis.topic, analysis.sentiment)}
    return render(request, "homepage.html", context)


# REST POST / advancedAnalysis.html
@require_http_methods(["POST"])
def advanced_results(request):
    try:
        corpus = _uploaded(request, "corpus")
        if corpus is None or not corpus.name.lower().endswith(".txt"):
            raise ValueError("Upload a .txt file to train the topic model on.")
        analysis = run_analysis(**_form_input(request), corpus=corpus)
    except (ValueError, *AnalysisError) as exc:
        return render(request, "advancedAnalysis.html", {"error": str(exc)}, status=400)
    return render(request, "results.html", {"analysis": analysis})
