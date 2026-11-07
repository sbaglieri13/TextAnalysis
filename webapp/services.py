from django.conf import settings

from nlp import pipeline, speech
from nlp.speech import TranscriptionError
from nlp.topics import CorpusTooSmallError, TopicModelNotTrainedError

from .models import Analysis

AnalysisError = (TranscriptionError, CorpusTooSmallError, TopicModelNotTrainedError)


def read_text_file(uploaded_file) -> str:
    return uploaded_file.read().decode("utf-8", errors="replace")


def run_analysis(*, text: str | None = None, audio=None, corpus=None) -> Analysis:
    source = Analysis.Source.AUDIO if audio is not None else Analysis.Source.TEXT
    if audio is not None:
        text = speech.transcribe(audio)

    if corpus is not None:
        result = pipeline.analyze_text_with_corpus(text, read_text_file(corpus))
        topic_model = Analysis.TopicModel.CUSTOM_CORPUS
    else:
        result = pipeline.analyze_text(text, settings.TOPIC_MODEL_DIR)
        topic_model = Analysis.TopicModel.PRETRAINED

    return Analysis.objects.create(
        source=source,
        topic_model=topic_model,
        text=result.text,
        sentiment=result.sentiment.label,
        sentiment_score=result.sentiment.score,
        sentiment_distribution=result.sentiment.distribution,
        sentences=[{"sentence": s.sentence, "label": s.label, "score": s.score} for s in result.sentiment.sentences],
        topic=result.topic,
        topic_probability=result.topic_probability,
        topic_words=result.topic_words,
    )
