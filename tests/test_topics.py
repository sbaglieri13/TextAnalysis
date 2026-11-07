import json

import pytest

from nlp import pipeline, topics


def test_trained_model_files_and_labels(trained_model_dir):
    summary = json.loads((trained_model_dir / topics.LABELS_FILE).read_text())
    assert len(summary) == topics.NUM_TOPICS
    for info in summary.values():
        assert info["label"]
        assert len(info["top_words"]) == topics.TOP_WORDS


def test_pretrained_prediction_is_deterministic(trained_model_dir):
    model = topics.get_pretrained_model(trained_model_dir)
    text = "The government and the president lost the election, the minister said."
    first, second = model.predict(text), model.predict(text)
    assert first == second
    assert 0 <= first.probability <= 1
    assert first.label in set(model.labels.values())


def test_pretrained_prediction_without_known_words(trained_model_dir):
    assert topics.get_pretrained_model(trained_model_dir).predict("Xyzzy qwerty.") is None


def test_missing_model_raises(tmp_path):
    with pytest.raises(topics.TopicModelNotTrainedError):
        topics.PretrainedTopicModel(tmp_path)


def test_custom_corpus_topic_words(romeo_corpus):
    prediction = topics.predict_with_corpus("O Romeo, I love thee, sweet love, good night.", romeo_corpus)
    assert prediction is not None
    assert len(prediction.words) == topics.TOP_WORDS
    assert prediction.label == " - ".join(prediction.words)


def test_custom_corpus_too_small():
    with pytest.raises(topics.CorpusTooSmallError):
        topics.predict_with_corpus("Hello there.", "Just one short sentence.")


def test_low_probability_topic_is_not_reported(monkeypatch, romeo_corpus):
    weak = topics.TopicPrediction("weak topic", pipeline.MIN_TOPIC_PROBABILITY, ["weak"])
    monkeypatch.setattr(topics, "predict_with_corpus", lambda text, corpus: weak)
    result = pipeline.analyze_text_with_corpus("Some text.", romeo_corpus)
    assert result.topic is None
    assert result.topic_probability is None
