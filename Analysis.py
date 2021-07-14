import Preprocessing as pp
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
import numpy as np
import pandas as pd
from itertools import chain
from langdetect import detect
from gensim import models
from gensim import corpora
from gensim.models import Phrases

topic_labels = ["News & Politics", "Law & Government", "Art", "Hobbies & Interests", "Entertainment",
                "People & Society", "Business", "Nature", "Fashion", "Work"]
sentiment_labels = ["POSITIVE", "NEUTRAL", "NEGATIVE"]


def sentiment_analysis_en(text):
    text = tokenize.sent_tokenize(text)

    sia = SentimentIntensityAnalyzer()

    pos_score = []
    neg_score = []
    neu_score = []

    for sent in text:
        sentiment = sia.polarity_scores(sent)
        pos_score.append(sentiment['pos'])
        neg_score.append(sentiment['neg'])
        neu_score.append(sentiment['neu'])

    score = [np.mean(pos_score) * 100, np.mean(neu_score) * 100, np.mean(neg_score) * 100]

    sentiment_label = sentiment_labels[score.index(max(score))]

    return sentiment_label, round(max(score), 2)


def sentiment_analysis_en_for_sentence(text):
    text = tokenize.sent_tokenize(text)

    sia = SentimentIntensityAnalyzer()

    sentiment_label_for_sent = []

    for sent in text:
        sentiment = sia.polarity_scores(sent)
        score = [sentiment['pos'], sentiment['neu'], sentiment['neg']]
        sentiment_label = sentiment_labels[score.index(max(score))]
        sentiment_label_for_sent.append([sent, sentiment_label, (round(max(score), 2)*100)])

    return sentiment_label_for_sent


def topic_modelling(data):
    if data is None:
        data = pd.read_csv('articles_bbc.csv')
        data = data.dropna().reset_index(drop=True)

        data['lang'] = data.articles.map(detect)
        data = data.loc[data.lang == 'en']

        data['sentences'] = data.articles.map(sent_tokenize)

        data['tokens'] = data['sentences'].map(
            lambda sentences: [pp.preprocessing_en(sentence) for sentence in sentences])

        data['tokens'] = data['tokens'].map(lambda sentences: list(chain.from_iterable(sentences)))
        tokens = data['tokens']
        bigram_model = Phrases(tokens)
        trigram_model = Phrases(bigram_model[tokens], min_count=1)
        tokens = list(trigram_model[bigram_model[tokens]])
    else:
        with open(data, 'r') as file:
            data = file.read().replace('\n', '')

        data = sent_tokenize(data)
        tokens = []
        for sentence in data:
            tokens.append(pp.preprocessing_en(sentence))

        tokens = list(tokens)

    dictionary_LDA = corpora.Dictionary(tokens)
    dictionary_LDA.filter_extremes(no_below=3)
    corpus = [dictionary_LDA.doc2bow(tok) for tok in tokens]

    np.random.seed(123456)
    lda_model = models.LdaModel(corpus, num_topics=10,
                                id2word=dictionary_LDA,
                                passes=4, alpha=[0.01] * 10,
                                eta=[0.01] * len(dictionary_LDA.keys()))

    return lda_model, dictionary_LDA


def topic_extraction(text, data):
    if data is None:
        lda_model, dictionary_LDA = topic_modelling(None)

        tokens = pp.preprocessing_en(text)
        topics = []
        for el in lda_model[dictionary_LDA.doc2bow(tokens)]:
            topics.append([topic_labels[el[0]], round((el[1] * 100), 2)])
        topics = sorted(topics, key=lambda x: x[1], reverse=True)

        return topics

    else:
        lda_model, dictionary_LDA = topic_modelling(data)
        tokens = pp.preprocessing_en(text)
        show_topics_list(lda_model)
        show_topics(lda_model, dictionary_LDA, tokens)


def show_topics_list(lda_model):
    for i, topic in lda_model.show_topics(formatted=True, num_topics=10, num_words=20):
        print(str(i) + ": " + topic)
    print()


def show_topics(lda_model, dictionary, tokens):
    topics = lda_model.show_topics(formatted=True, num_topics=10, num_words=20)
    print(
        pd.DataFrame(
            [(el[0], round(el[1], 2), topics[el[0]][1]) for el in lda_model[dictionary.doc2bow(tokens)]],
            columns=['topic #', 'weight', 'words in topic']))
