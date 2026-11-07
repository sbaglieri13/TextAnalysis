from __future__ import annotations

import json
import logging
import threading
from dataclasses import dataclass
from itertools import chain
from pathlib import Path

import numpy as np
from gensim.corpora import Dictionary
from gensim.models import LdaModel, Phrases
from gensim.models.phrases import FrozenPhrases
from nltk.tokenize import sent_tokenize

from .preprocessing import preprocess

logger = logging.getLogger(__name__)

NUM_TOPICS = 10
PASSES = 20
ITERATIONS = 200
SEED = 123456
MIN_DOCUMENT_FREQUENCY = 3
TOP_WORDS = 10

MODEL_FILE = "lda.model"
BIGRAM_FILE = "bigrams.phraser"
TRIGRAM_FILE = "trigrams.phraser"
LABELS_FILE = "topic_labels.json"

SEED_KEYWORDS: dict[str, set[str]] = {
    "Travel": {
        "travel",
        "tourist",
        "tourism",
        "flight",
        "airport",
        "airline",
        "holiday",
        "hotel",
        "visitor",
        "passenger",
        "trip",
        "destination",
        "beach",
    },
    "Health - Disease": {
        "health",
        "patient",
        "hospital",
        "disease",
        "doctor",
        "cancer",
        "virus",
        "drug",
        "medical",
        "treatment",
        "infection",
        "vaccine",
        "nurse",
    },
    "Nature - Environment": {
        "nature",
        "animal",
        "species",
        "specie",
        "wildlife",
        "forest",
        "bird",
        "plant",
        "tree",
        "ocean",
        "river",
        "park",
        "fish",
        "wild",
    },
    "Science": {
        "science",
        "scientist",
        "research",
        "researcher",
        "study",
        "space",
        "technology",
        "data",
        "experiment",
        "planet",
        "discovery",
        "computer",
    },
    "Lifestyle & Leisure": {
        "food",
        "lifestyle",
        "leisure",
        "restaurant",
        "home",
        "sport",
        "game",
        "team",
        "player",
        "club",
        "fashion",
        "holiday",
    },
    "Arts, Culture & Entertainment": {
        "film",
        "music",
        "book",
        "artist",
        "award",
        "theatre",
        "actor",
        "show",
        "star",
        "album",
        "festival",
        "culture",
        "song",
        "writer",
        "movie",
    },
    "Business": {
        "business",
        "company",
        "market",
        "bank",
        "price",
        "economy",
        "firm",
        "sale",
        "investor",
        "profit",
        "trade",
        "deal",
        "share",
        "growth",
    },
    "News & Politics": {
        "government",
        "election",
        "minister",
        "party",
        "president",
        "vote",
        "police",
        "court",
        "policy",
        "leader",
        "political",
        "campaign",
        "law",
    },
    "Human interests": {
        "people",
        "child",
        "woman",
        "family",
        "school",
        "story",
        "young",
        "community",
        "life",
        "mother",
        "friend",
        "student",
    },
    "Environmental issue & Environmental pollution": {
        "climate",
        "pollution",
        "emission",
        "carbon",
        "plastic",
        "waste",
        "energy",
        "warming",
        "environmental",
        "fuel",
    },
}


class TopicModelNotTrainedError(RuntimeError):
    pass


class CorpusTooSmallError(ValueError):
    pass


@dataclass(frozen=True)
class TopicPrediction:
    label: str
    probability: float
    words: list[str]


def _train_lda(corpus: list, dictionary: Dictionary) -> LdaModel:
    return LdaModel(
        corpus,
        num_topics=NUM_TOPICS,
        id2word=dictionary,
        passes=PASSES,
        iterations=ITERATIONS,
        alpha=[0.01] * NUM_TOPICS,
        eta=0.01,
        random_state=SEED,
    )


def _document_topics(model: LdaModel, bow: list) -> list[tuple[int, float]]:
    model.random_state = np.random.RandomState(SEED)
    return model.get_document_topics(bow, minimum_probability=0.0)


def _top_words(model: LdaModel, topic_id: int, topn: int = TOP_WORDS) -> list[str]:
    return [word for word, _ in model.show_topic(topic_id, topn=topn)]


def label_topics(model: LdaModel, topn: int = 50) -> dict[int, str]:
    labels = {}
    for topic_id in range(model.num_topics):
        terms = model.show_topic(topic_id, topn=topn)
        scores = {
            label: sum(p for term, p in terms if seeds & set(term.split("_"))) for label, seeds in SEED_KEYWORDS.items()
        }
        best_label, best_score = max(scores.items(), key=lambda item: item[1])
        labels[topic_id] = best_label if best_score > 0 else f"Topic {topic_id}"
    return labels


def train_pretrained_model(articles: list[str], output_dir: Path) -> dict[int, dict]:
    documents = [list(chain.from_iterable(preprocess(s) for s in sent_tokenize(article))) for article in articles]
    bigrams = Phrases(documents).freeze()
    trigrams = Phrases(bigrams[documents], min_count=1).freeze()
    documents = [trigrams[bigrams[doc]] for doc in documents]

    dictionary = Dictionary(documents)
    dictionary.filter_extremes(no_below=MIN_DOCUMENT_FREQUENCY)
    corpus = [dictionary.doc2bow(doc) for doc in documents]
    model = _train_lda(corpus, dictionary)

    labels = label_topics(model)
    summary = {
        topic_id: {"label": labels[topic_id], "top_words": _top_words(model, topic_id)}
        for topic_id in range(model.num_topics)
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    model.save(str(output_dir / MODEL_FILE))
    bigrams.save(str(output_dir / BIGRAM_FILE))
    trigrams.save(str(output_dir / TRIGRAM_FILE))
    (output_dir / LABELS_FILE).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


class PretrainedTopicModel:
    def __init__(self, model_dir: Path):
        if not (model_dir / MODEL_FILE).exists():
            raise TopicModelNotTrainedError(
                f"No topic model found in '{model_dir}'. Train it with: python manage.py train_topic_model"
            )
        self.model = LdaModel.load(str(model_dir / MODEL_FILE))
        self.bigrams = FrozenPhrases.load(str(model_dir / BIGRAM_FILE))
        self.trigrams = FrozenPhrases.load(str(model_dir / TRIGRAM_FILE))
        summary = json.loads((model_dir / LABELS_FILE).read_text(encoding="utf-8"))
        self.labels = {int(topic_id): info["label"] for topic_id, info in summary.items()}
        self._lock = threading.Lock()

    def predict(self, text: str) -> TopicPrediction | None:
        tokens = self.trigrams[self.bigrams[preprocess(text)]]
        bow = self.model.id2word.doc2bow(tokens)
        if not bow:
            return None
        with self._lock:
            topics = _document_topics(self.model, bow)

        by_label: dict[str, float] = {}
        for topic_id, probability in topics:
            label = self.labels[topic_id]
            by_label[label] = by_label.get(label, 0.0) + float(probability)
        label, probability = max(by_label.items(), key=lambda item: item[1])
        best_topic = max(topics, key=lambda item: item[1])[0]
        return TopicPrediction(label, round(probability, 4), _top_words(self.model, best_topic))


_loaded_models: dict[Path, PretrainedTopicModel] = {}
_load_lock = threading.Lock()


def get_pretrained_model(model_dir: Path) -> PretrainedTopicModel:
    with _load_lock:
        if model_dir not in _loaded_models:
            logger.info("Loading topic model from %s", model_dir)
            _loaded_models[model_dir] = PretrainedTopicModel(model_dir)
        return _loaded_models[model_dir]


def predict_with_corpus(text: str, corpus_text: str) -> TopicPrediction | None:
    documents = [preprocess(sentence) for sentence in sent_tokenize(corpus_text)]
    dictionary = Dictionary(documents)
    dictionary.filter_extremes(no_below=MIN_DOCUMENT_FREQUENCY)
    corpus = [bow for bow in (dictionary.doc2bow(doc) for doc in documents) if bow]
    if len(dictionary) < NUM_TOPICS or len(corpus) < NUM_TOPICS:
        raise CorpusTooSmallError("The uploaded file is too small to extract topics: use a longer English text.")

    model = _train_lda(corpus, dictionary)
    bow = dictionary.doc2bow(preprocess(text))
    if not bow:
        return None
    topic_id, probability = max(_document_topics(model, bow), key=lambda item: item[1])
    words = _top_words(model, topic_id)
    return TopicPrediction(" - ".join(words), round(float(probability), 4), words)
