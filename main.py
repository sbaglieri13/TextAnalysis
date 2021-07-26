import os
import django
import analysis as an
import speechRecognition as sr

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TextAnalysis.settings')
django.setup()

from webapp.models import Prediction


def text_analysis(text):
    sentiment = an.sentiment_analysis_en(text)
    topic = an.topic_extraction(text, None)
    return sentiment, topic


def speech_analysis():
    text = sr.run()
    sentiment = an.sentiment_analysis_en(text)
    topic = an.topic_extraction(text, None)
    return text, sentiment, topic


def analysis_with_data(text, data):
    sentiment = an.sentiment_analysis_en(text)
    sentiment_for_sent = an.sentiment_analysis_en_for_sentence(text)
    topics = an.topic_extraction(text, 'data/' + str(data).replace(" ", "_"))
    return sentiment, sentiment_for_sent, topics


def analysis(text):
    text = "".join(text)
    if text != "":
        sentiment, topic = text_analysis(text)
    else:
        text, sentiment, topic = speech_analysis()

    if topic[1] < 50:
        prediction = Prediction(
            text=text,
            sentiment=sentiment[0],
            sentiment_acc=sentiment[1],
            topic=None,
            topic_acc=None
        )

    else:
        prediction = Prediction(
            text=text,
            sentiment=sentiment[0],
            sentiment_acc=sentiment[1],
            topic=topic[0],
            topic_acc=topic[1]
        )

    prediction.save()


def data_analysis(text, data):
    text = "".join(text)
    if text != "":
        sentiment, sentiment_for_sent, topics = analysis_with_data(text, data)
    else:
        text = sr.run()
        sentiment, sentiment_for_sent, topics = analysis_with_data(text, data)

    return text, sentiment, sentiment_for_sent, topics
