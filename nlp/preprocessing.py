from functools import lru_cache
from pathlib import Path

from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer

CUSTOM_STOP_WORDS_FILE = Path(__file__).with_name("stop_words_english.txt")
MIN_TOKEN_LENGTH = 4

_tokenizer = TreebankWordTokenizer()
_lemmatizer = WordNetLemmatizer()

# mapping logic:
#   pos_tags that begin with J are adjectives
#                       with V are verbs
#                       with N are nouns
#                       with R are adverbs
_POS_MAP = {"J": "a", "N": "n", "V": "v", "R": "r"}
_DEFAULT_POS = "n"


@lru_cache(maxsize=1)
def stop_words() -> frozenset[str]:
    custom = CUSTOM_STOP_WORDS_FILE.read_text(encoding="utf-8").splitlines()
    return frozenset(stopwords.words("english")) | {w.strip() for w in custom if w.strip()}


def to_wordnet_pos(treebank_tag: str) -> str:
    return _POS_MAP.get(treebank_tag[:1].upper(), _DEFAULT_POS)


def preprocess(text: str) -> list[str]:
    # Word tokenization
    tokens = _tokenizer.tokenize(text.lower())

    # Normalization
    lemmas = (_lemmatizer.lemmatize(word, pos=to_wordnet_pos(tag)) for word, tag in pos_tag(tokens))

    # Removing stopwords and punctuation
    excluded = stop_words()
    return [lemma for lemma in lemmas if lemma.isalpha() and len(lemma) >= MIN_TOKEN_LENGTH and lemma not in excluded]
