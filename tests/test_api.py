import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from nlp.speech import TranscriptionError
from tests.conftest import SAMPLES, make_wav
from webapp.models import Analysis

pytestmark = pytest.mark.django_db
URL = "/api/analyses/"


@pytest.fixture
def client():
    return APIClient()


def test_health(client):
    assert client.get("/api/health/").json() == {"status": "ok"}


def test_analyze_text(client, topic_model):
    response = client.post(URL, {"text": "I love this beautiful film. The actors were great!"}, format="json")
    assert response.status_code == 201
    body = response.json()
    assert body["sentiment"] == "POSITIVE"
    assert body["source"] == "text"
    assert body["topic_model"] == "pretrained"
    assert len(body["sentences"]) == 2
    assert Analysis.objects.filter(id=body["id"]).exists()


def test_list_and_retrieve(client, topic_model):
    created = client.post(URL, {"text": "What a sad day."}, format="json").json()
    listing = client.get(URL).json()
    assert listing["count"] == 1
    assert client.get(f"{URL}{created['id']}/").json()["text"] == "What a sad day."


def test_unknown_id_returns_404(client):
    assert client.get(f"{URL}00000000-0000-0000-0000-000000000000/").status_code == 404


@pytest.mark.parametrize("payload", [{}, {"text": ""}])
def test_text_or_audio_is_required(client, payload):
    assert client.post(URL, payload, format="json").status_code == 400


def test_text_and_audio_together_are_rejected(client):
    audio = SimpleUploadedFile("speech.wav", make_wav(), content_type="audio/wav")
    assert client.post(URL, {"text": "hi", "audio": audio}, format="multipart").status_code == 400


def test_audio_extension_is_validated(client):
    audio = SimpleUploadedFile("speech.mp3", b"data", content_type="audio/mpeg")
    response = client.post(URL, {"audio": audio}, format="multipart")
    assert response.status_code == 400
    assert "audio" in response.json()


def test_analyze_audio(client, topic_model, monkeypatch):
    monkeypatch.setattr("webapp.services.speech.transcribe", lambda audio: "I am very happy today.")
    audio = SimpleUploadedFile("speech.wav", make_wav(), content_type="audio/wav")
    response = client.post(URL, {"audio": audio}, format="multipart")
    assert response.status_code == 201
    assert response.json()["source"] == "audio"
    assert response.json()["text"] == "I am very happy today."


def test_transcription_error_returns_422(client, topic_model, monkeypatch):
    def fail(audio):
        raise TranscriptionError("The speech in the audio could not be understood.")

    monkeypatch.setattr("webapp.services.speech.transcribe", fail)
    audio = SimpleUploadedFile("speech.wav", make_wav(), content_type="audio/wav")
    response = client.post(URL, {"audio": audio}, format="multipart")
    assert response.status_code == 422


def test_analyze_with_custom_corpus(client):
    corpus = SimpleUploadedFile("romeo.txt", (SAMPLES / "romeo-and-juliet.txt").read_bytes())
    response = client.post(URL, {"text": "Good night, sweet love.", "corpus": corpus}, format="multipart")
    assert response.status_code == 201
    assert response.json()["topic_model"] == "custom_corpus"


def test_corpus_too_small_returns_422(client):
    corpus = SimpleUploadedFile("tiny.txt", b"One sentence only.")
    response = client.post(URL, {"text": "Hello.", "corpus": corpus}, format="multipart")
    assert response.status_code == 422


def test_missing_topic_model_returns_503(client, settings, tmp_path):
    settings.TOPIC_MODEL_DIR = tmp_path
    response = client.post(URL, {"text": "Hello world."}, format="json")
    assert response.status_code == 503
    assert "train_topic_model" in response.json()["detail"]
