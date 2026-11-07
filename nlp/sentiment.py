from dataclasses import dataclass
from functools import lru_cache

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize

POSITIVE, NEUTRAL, NEGATIVE = "POSITIVE", "NEUTRAL", "NEGATIVE"
LABELS = (POSITIVE, NEUTRAL, NEGATIVE)
THRESHOLD = 0.05


@dataclass(frozen=True)
class SentenceSentiment:
    sentence: str
    label: str
    score: float


@dataclass(frozen=True)
class SentimentResult:
    label: str
    score: float
    distribution: dict[str, float]
    sentences: list[SentenceSentiment]


@lru_cache(maxsize=1)
def _analyzer() -> SentimentIntensityAnalyzer:
    return SentimentIntensityAnalyzer()


def label_for(score: float) -> str:
    if score >= THRESHOLD:
        return POSITIVE
    if score <= -THRESHOLD:
        return NEGATIVE
    return NEUTRAL


def analyze_sentences(text: str) -> list[SentenceSentiment]:
    analyzer = _analyzer()
    results = []
    for sentence in sent_tokenize(text):
        score = analyzer.polarity_scores(sentence)["compound"]
        results.append(SentenceSentiment(sentence, label_for(score), round(score, 4)))
    return results


def analyze(text: str) -> SentimentResult:
    sentences = analyze_sentences(text)
    if not sentences:
        return SentimentResult(NEUTRAL, 0.0, {label: 0.0 for label in LABELS}, [])

    score = sum(s.score for s in sentences) / len(sentences)
    distribution = {
        label: round(100 * sum(s.label == label for s in sentences) / len(sentences), 2) for label in LABELS
    }
    return SentimentResult(label_for(score), round(score, 4), distribution, sentences)
