from dataclasses import dataclass, field
from pathlib import Path

from . import sentiment, topics

MIN_TOPIC_PROBABILITY = 0.5


@dataclass(frozen=True)
class AnalysisResult:
    text: str
    sentiment: sentiment.SentimentResult
    topic: str | None = None
    topic_probability: float | None = None
    topic_words: list[str] = field(default_factory=list)


def _result(text: str, prediction: topics.TopicPrediction | None) -> AnalysisResult:
    result = sentiment.analyze(text)
    if prediction is None or prediction.probability <= MIN_TOPIC_PROBABILITY:
        return AnalysisResult(text, result)
    return AnalysisResult(text, result, prediction.label, prediction.probability, prediction.words)


def analyze_text(text: str, model_dir: Path) -> AnalysisResult:
    prediction = topics.get_pretrained_model(model_dir).predict(text)
    return _result(text, prediction)


def analyze_text_with_corpus(text: str, corpus_text: str) -> AnalysisResult:
    return _result(text, topics.predict_with_corpus(text, corpus_text))
