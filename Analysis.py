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

    label = ["POSITIVE", "NEUTRAL", "NEGATIVE"]
    score = [np.mean(pos_score) * 100, np.mean(neu_score) * 100, np.mean(neg_score) * 100]

    sentiment_label = label[score.index(max(score))]
    return sentiment_label, max(score)


def sentiment_analysis_en_for_sentence(text):

    text = tokenize.sent_tokenize(text)

    sia = SentimentIntensityAnalyzer()

    sentiment_label_for_sent = []

    label = ["POSITIVE", "NEUTRAL", "NEGATIVE"]

    for sent in text:
        sentiment = sia.polarity_scores(sent)
        score = [sentiment['pos'], sentiment['neu'], sentiment['neg']]
        sentiment_label = label[score.index(max(score))]
        sentiment_label_for_sent.append([sent, sentiment_label, max(score)])

    return sentiment_label_for_sent


def topic_modelling():

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

    dictionary_LDA = corpora.Dictionary(tokens)
    dictionary_LDA.filter_extremes(no_below=3)
    corpus = [dictionary_LDA.doc2bow(tok) for tok in tokens]

    np.random.seed(123456)
    num_topics = 20
    lda_model = models.LdaModel(corpus, num_topics=num_topics,
                                id2word=dictionary_LDA,
                                passes=4, alpha=[0.01] * num_topics,
                                eta=[0.01] * len(dictionary_LDA.keys()))

    for i, topic in lda_model.show_topics(formatted=True, num_topics=num_topics, num_words=20):
        print(str(i) + ": " + topic)
        print()

    return lda_model, dictionary_LDA, num_topics


def topic_extraction(text):

    lda_model, dictionary_LDA, num_topics = topic_modelling()

    tokens = pp.preprocessing_en(text)
    topics = lda_model.show_topics(formatted=True, num_topics=num_topics, num_words=20)
    print(
        pd.DataFrame([(el[0], round(el[1], 2), topics[el[0]][1]) for el in lda_model[dictionary_LDA.doc2bow(tokens)]],
                     columns=['topic #', 'weight', 'words in topic']))
