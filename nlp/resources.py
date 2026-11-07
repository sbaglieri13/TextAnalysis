import nltk

NLTK_PACKAGES = {
    "punkt_tab": "tokenizers/punkt_tab",
    "vader_lexicon": "sentiment/vader_lexicon.zip",
    "averaged_perceptron_tagger_eng": "taggers/averaged_perceptron_tagger_eng",
    "wordnet": "corpora/wordnet.zip",
    "stopwords": "corpora/stopwords",
}


def missing_nltk_packages() -> list[str]:
    missing = []
    for package, resource in NLTK_PACKAGES.items():
        try:
            nltk.data.find(resource)
        except LookupError:
            missing.append(package)
    return missing


def ensure_nltk_data(download_dir: str | None = None) -> list[str]:
    missing = missing_nltk_packages()
    for package in missing:
        nltk.download(package, download_dir=download_dir, quiet=True)
    return missing
