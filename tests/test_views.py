import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from tests.conftest import SAMPLES
from webapp.models import Analysis
from webapp.views import stage_scene

pytestmark = pytest.mark.django_db


def test_pages_render(client):
    assert client.get("/").status_code == 200
    assert client.get("/advancedAnalysis/").status_code == 200


def test_analyze_text_sets_stage_scene(client, monkeypatch):
    analysis = Analysis(text="Animals.", sentiment="NEGATIVE", sentiment_score=-0.5, topic="Nature - Environment")
    monkeypatch.setattr("webapp.views.run_analysis", lambda **kwargs: analysis)
    response = client.post("/results_analysis", {"text": "Animals at risk."})
    assert response.status_code == 200
    assert b"styleTopicNatureNegative.css" in response.content
    assert b"nature-tense.m4a" in response.content


def test_analyze_empty_text_shows_error(client):
    response = client.post("/results_analysis", {"text": "   "})
    assert response.status_code == 400
    assert b"ta-alert" in response.content


def test_advanced_results_page(client):
    corpus = SimpleUploadedFile("romeo.txt", (SAMPLES / "romeo-and-juliet.txt").read_bytes())
    response = client.post(
        "/advancedAnalysis/results_data_analysis", {"text": "Good night, sweet love.", "corpus": corpus}
    )
    assert response.status_code == 200
    assert b"Result of analysis" in response.content


def test_advanced_analysis_requires_corpus(client):
    response = client.post("/advancedAnalysis/results_data_analysis", {"text": "Hello."})
    assert response.status_code == 400


@pytest.mark.parametrize(
    ("topic", "sentiment", "css", "audio"),
    [
        ("Nature - Environment", "NEGATIVE", "styleTopicNatureNegative.css", "nature-tense.m4a"),
        ("Nature - Environment", "NEUTRAL", "styleTopicNatureNeutral.css", "nature.m4a"),
        ("Environmental issue & Environmental pollution", "POSITIVE", "styleTopicNaturePositive.css", "nature.m4a"),
        ("Arts, Culture & Entertainment", "NEGATIVE", "styleTopicArtsNegative.css", "arts-and-culture-tense.m4a"),
        ("News & Politics", "NEGATIVE", "styleTopicNewsNegative.css", "news.m4a"),
    ],
)
def test_stage_scene(topic, sentiment, css, audio):
    scene = stage_scene(topic, sentiment)
    assert scene["css"].endswith(css)
    assert scene["audio"].endswith(audio)


def test_stage_scene_for_other_topics():
    assert stage_scene("Business", "POSITIVE") is None
    assert stage_scene(None, "POSITIVE") is None


def test_every_scene_file_exists():
    from django.contrib.staticfiles import finders

    for topic in ("Nature - Environment", "Arts, Culture & Entertainment", "News & Politics"):
        for sentiment in ("POSITIVE", "NEUTRAL", "NEGATIVE"):
            scene = stage_scene(topic, sentiment)
            assert finders.find(scene["css"]), scene["css"]
            assert finders.find(scene["audio"]), scene["audio"]
