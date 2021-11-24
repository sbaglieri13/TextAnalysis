import analysis as an
import speechRecognition as sr


def analysis_without_data(text):
    sent = an.sentiment_analysis_en(text)
    top = an.topic_extraction(text, None)
    sentiment = sent[0]
    sentiment_acc = sent[1]
    topic = top[0]
    topic_acc = top[1]
    return sentiment, sentiment_acc, topic, topic_acc


def analysis_with_data(text, data):
    sent = an.sentiment_analysis_en(text)
    sentiment = sent[0]
    sentiment_acc = sent[1]
    sentiment_for_sent = an.sentiment_analysis_en_for_sentence(text)
    topics = an.topic_extraction(text, data)
    topic = topics[0][1]

    chars = "0123456789+*.\"\\"
    for c in chars:
        topic = topic.replace(c, "")

    topic = " ".join(topic.split())
    topic = topic.replace(" ", " - ")

    topic_acc = topics[0][0]
    return sentiment, sentiment_acc, sentiment_for_sent, topic, topic_acc


def analysis(text, audio_file):
    if audio_file is None:
        text = "".join(text)
    elif text is None:
        text = sr.run(audio_file)

    sentiment, sentiment_acc, topic, topic_acc = analysis_without_data(text)

    if sentiment_acc <= 50:
        sentiment = None
        sentiment_acc = None

    if topic_acc <= 50:
        topic = None
        topic_acc = None

    return text, sentiment, sentiment_acc, topic, topic_acc


def data_analysis(text, audio_file, data):
    if audio_file is None:
        text = "".join(text)
    elif text is None:
        text = sr.run(audio_file)

    sentiment, sentiment_acc, sentiment_for_sent, topic, topic_acc = analysis_with_data(text, data)
    topic_acc = round(topic_acc * 100, 2)

    if sentiment_acc <= 50:
        sentiment = None
        sentiment_acc = None

    if topic_acc <= 50:
        topic = None
        topic_acc = None

    return text, sentiment, sentiment_acc, sentiment_for_sent, topic, topic_acc
