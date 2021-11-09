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
    sentiment = an.sentiment_analysis_en(text)
    sentiment_for_sent = an.sentiment_analysis_en_for_sentence(text)
    topics = an.topic_extraction(text, data)
    return sentiment, sentiment_for_sent, topics


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

    sentiment, sentiment_for_sent, topics = analysis_with_data(text, data)

    return text, sentiment, sentiment_for_sent, topics
