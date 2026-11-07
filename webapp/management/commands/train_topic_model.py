import time
from pathlib import Path

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from langdetect import DetectorFactory, LangDetectException, detect

from nlp.topics import train_pretrained_model


def is_english(text: str) -> bool:
    try:
        return detect(text) == "en"
    except LangDetectException:
        return False


class Command(BaseCommand):
    help = "Train the LDA topic model on the BBC articles corpus and save it to disk."

    def add_arguments(self, parser):
        parser.add_argument("--corpus", type=Path, default=settings.TRAINING_CORPUS)
        parser.add_argument("--output", type=Path, default=settings.TOPIC_MODEL_DIR)

    def handle(self, *args, **options):
        DetectorFactory.seed = 0
        start = time.perf_counter()

        articles = pd.read_csv(options["corpus"], usecols=["articles"])["articles"].dropna()
        english = [a for a in articles if is_english(a)]
        self.stdout.write(f"Training on {len(english)}/{len(articles)} English articles...")

        summary = train_pretrained_model(english, options["output"])

        for topic_id, info in summary.items():
            self.stdout.write(f"  [{topic_id}] {info['label']:<46} {', '.join(info['top_words'][:6])}")
        elapsed = time.perf_counter() - start
        self.stdout.write(self.style.SUCCESS(f"Model saved to {options['output']} ({elapsed:.0f}s)"))
