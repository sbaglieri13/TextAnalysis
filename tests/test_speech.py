import io

import pytest
import speech_recognition as sr

from nlp import speech
from tests.conftest import make_wav


def test_transcribe_wav(monkeypatch):
    monkeypatch.setattr(sr.Recognizer, "recognize_google", lambda self, audio, language: "hello world")
    assert speech.transcribe(io.BytesIO(make_wav())) == "hello world"


def test_unintelligible_audio(monkeypatch):
    def fail(self, audio, language):
        raise sr.UnknownValueError()

    monkeypatch.setattr(sr.Recognizer, "recognize_google", fail)
    with pytest.raises(speech.TranscriptionError, match="could not be understood"):
        speech.transcribe(io.BytesIO(make_wav()))


def test_invalid_audio_file():
    with pytest.raises(speech.TranscriptionError, match="Unsupported audio file"):
        speech.transcribe(io.BytesIO(b"this is not audio"))
