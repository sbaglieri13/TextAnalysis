import nltk

import preprocessing as pp
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

nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')

topic_labels = ["Travel", "Health - Disease", "Nature - Environment", "Science", "Lifestyle & Leisure",
                "Arts, Culture & Entertainment", "Business", "News & Politics", "Human interests", "Environmental "
                                                                                                   "issue & "
                                                                                                   "Environmental "
                                                                                                   "pollution"]
sentiment_labels = ["POSITIVE", "NEUTRAL", "NEGATIVE"]

lda_model_articles_bbc = None
dictionary_LDA_articles_bbc = None


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
        sentiment_label_for_sent.append([sent, sentiment_label, (round(max(score), 2) * 100)])

    return sentiment_label_for_sent


def topic_modelling_load():
    data = pd.read_csv('articles_bbc.csv')
    data = data.dropna().reset_index(drop=True)

    data['lang'] = data.articles.map(detect)
    data = data.loc[data.lang == 'en']

    data['sentences'] = data.articles.map(sent_tokenize)

    data['tokens'] = data['sentences'].map(
        lambda sentences: [pp.preprocessing_en(sent) for sent in sentences])

    data['tokens'] = data['tokens'].map(lambda sentences: list(chain.from_iterable(sentences)))
    tokens = data['tokens']
    bigram_model = Phrases(tokens)
    trigram_model = Phrases(bigram_model[tokens], min_count=1)
    tokens = list(trigram_model[bigram_model[tokens]])

    dictionary_LDA = corpora.Dictionary(tokens)
    dictionary_LDA.filter_extremes(no_below=3)
    corpus = [dictionary_LDA.doc2bow(tok) for tok in tokens]

    np.random.seed(123456)
    lda_model = models.LdaModel(corpus, num_topics=10,
                                id2word=dictionary_LDA,
                                passes=4, alpha=[0.01] * 10,
                                eta=[0.01] * len(dictionary_LDA.keys()))

    global lda_model_articles_bbc
    global dictionary_LDA_articles_bbc
    lda_model_articles_bbc = lda_model
    dictionary_LDA_articles_bbc = dictionary_LDA


def topic_modelling(data):
    if data is None and not lda_model_articles_bbc:
        topic_modelling_load()
        return lda_model_articles_bbc, dictionary_LDA_articles_bbc
    elif data is None and lda_model_articles_bbc:
        return lda_model_articles_bbc, dictionary_LDA_articles_bbc
    else:
        data = data.read().decode()

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

        # show_topics_list(lda_model)
        return topics[0]

    else:
        lda_model, dictionary_LDA = topic_modelling(data)
        tokens = pp.preprocessing_en(text)
        # show_topics_list(lda_model)
        # show_topics(lda_model, dictionary_LDA, tokens)
        return topics_list(lda_model, dictionary_LDA, tokens)


def show_topics_list(lda_model):
    for i, topic in lda_model.show_topics(formatted=True, num_topics=10, num_words=30):
        print(str(i) + ": " + topic)
    print()


def show_topics(lda_model, dictionary, tokens):
    topics = lda_model.show_topics(formatted=True, num_topics=10, num_words=30)
    print(
        pd.DataFrame(
            [(el[0], round(el[1], 2), topics[el[0]][1]) for el in lda_model[dictionary.doc2bow(tokens)]],
            columns=['topic #', 'weight', 'words in topic']))


def topics_list(lda_model, dictionary, tokens):
    topics = lda_model.show_topics(formatted=True, num_topics=10, num_words=30)
    topics = [(round(el[1], 2), topics[el[0]][1]) for el in lda_model[dictionary.doc2bow(tokens)]]
    topics = sorted(topics, key=lambda x: x[0], reverse=True)
    return topics
