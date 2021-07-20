import os
from sys import argv
import django
import analysis as an
import speechRecognition as sr

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TextAnalysis.settings')
django.setup()

from webapp.models import PredictionText, PredictionSpeech


def text_analysis(text):
    sentiment = an.sentiment_analysis_en(text)
    topic = an.topic_extraction(text, None)
    return sentiment, topic


def speech_analysis():
    text = sr.run()
    sentiment = an.sentiment_analysis_en(text)
    topic = an.topic_extraction(text, None)
    return text, sentiment, topic


def main(text):
    text = " ".join(text)

    if text != "":
        sentiment, topic = text_analysis(text)
        if topic[1] < 50:
            prediction = PredictionText(
                text=text,
                sentiment=sentiment[0],
                sentiment_acc=sentiment[1],
                topic=None,
                topic_acc=None
            )

        else:
            prediction = PredictionText(
                text=text,
                sentiment=sentiment[0],
                sentiment_acc=sentiment[1],
                topic=topic[0],
                topic_acc=topic[1]
            )

        prediction.save()

    else:
        text, sentiment, topic = speech_analysis()
        if topic[1] < 50:
            prediction = PredictionSpeech(
                speech_text=text,
                sentiment=sentiment[0],
                sentiment_acc=sentiment[1],
                topic=None,
                topic_acc=None
            )

        else:
            prediction = PredictionSpeech(
                speech_text=text,
                sentiment=sentiment[0],
                sentiment_acc=sentiment[1],
                topic=topic[0],
                topic_acc=topic[1]
            )

        prediction.save()


if __name__ == '__main__':
    main(argv[1:])
