from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np


def sentiment_analysis_en(text):
    # print("Text before sent_tokenize: ", text)
    text = tokenize.sent_tokenize(text)
    # print("Text after sent_tokenize: ", text)

    sia = SentimentIntensityAnalyzer()

    pos_score = []
    neg_score = []
    neu_score = []

    for sent in text:
        sentiment = sia.polarity_scores(sent)
        pos_score.append(sentiment['pos'])
        neg_score.append(sentiment['neg'])
        neu_score.append(sentiment['neu'])

    label = ["POSITIVE", "NEUTRAL", "NEGATIVE"]
    score = [np.mean(pos_score) * 100, np.mean(neu_score) * 100, np.mean(neg_score) * 100]

    sentiment_label = label[score.index(max(score))]
    return sentiment_label, max(score)


