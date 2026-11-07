import io
import wave
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ROOT / "data" / "samples"


@pytest.fixture(scope="session")
def romeo_corpus() -> str:
    return (SAMPLES / "romeo-and-juliet.txt").read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def trained_model_dir(tmp_path_factory) -> Path:
    from nlp.topics import train_pretrained_model

    articles = pd.read_csv(ROOT / "data" / "articles_bbc.csv", usecols=["articles"])["articles"].dropna()
    output = tmp_path_factory.mktemp("model")
    train_pretrained_model(list(articles[:80]), output)
    return output


@pytest.fixture
def topic_model(settings, trained_model_dir):
    settings.TOPIC_MODEL_DIR = trained_model_dir
    return trained_model_dir


def make_wav(seconds: float = 0.5, rate: int = 16000) -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes(b"\x00\x00" * int(seconds * rate))
    return buffer.getvalue()
