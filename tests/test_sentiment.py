import pytest

from nlp import sentiment


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("I love this wonderful, beautiful day!", sentiment.POSITIVE),
        ("This is a terrible, horrible and sad disaster.", sentiment.NEGATIVE),
        ("The meeting is on Tuesday.", sentiment.NEUTRAL),
    ],
)
def test_overall_label(text, expected):
    assert sentiment.analyze(text).label == expected


def test_label_thresholds():
    assert sentiment.label_for(0.05) == sentiment.POSITIVE
    assert sentiment.label_for(0.0) == sentiment.NEUTRAL
    assert sentiment.label_for(-0.05) == sentiment.NEGATIVE


def test_per_sentence_results_and_distribution():
    result = sentiment.analyze("I love it. I hate it. It is a table.")
    assert [s.label for s in result.sentences] == [sentiment.POSITIVE, sentiment.NEGATIVE, sentiment.NEUTRAL]
    assert sum(result.distribution.values()) == pytest.approx(100, abs=0.1)
    assert -1 <= result.score <= 1


def test_empty_text_is_neutral():
    result = sentiment.analyze("")
    assert result.label == sentiment.NEUTRAL
    assert result.sentences == []
