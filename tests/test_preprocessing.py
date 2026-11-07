from nlp.preprocessing import preprocess, to_wordnet_pos


def test_preprocess_lowercases_lemmatizes_and_drops_stop_words():
    tokens = preprocess("The Scientists STUDIED the ancient forests and the children, 123 times!")
    assert tokens == ["scientist", "ancient", "forest", "child"]
    assert all(token.isalpha() and token.islower() for token in tokens)


def test_preprocess_drops_short_tokens_and_punctuation():
    assert preprocess("A cat, a dog... ok?!") == []


def test_preprocess_empty_text():
    assert preprocess("") == []


def test_wordnet_pos_mapping():
    assert to_wordnet_pos("JJ") == "a"
    assert to_wordnet_pos("VBD") == "v"
    assert to_wordnet_pos("RB") == "r"
    assert to_wordnet_pos("NNS") == "n"
    assert to_wordnet_pos("XYZ") == "n"
