from nltk import tokenize
from nltk import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.corpus import stopwords


def preprocessing_en(text):
    # Word tokenization
    tokenizer = tokenize.TreebankWordTokenizer()
    tokens = tokenizer.tokenize(text.lower())

    # Normalization
    lemmatizer = WordNetLemmatizer()
    tagged_tokens = pos_tag(tokens)
    lemma_list = []
    for word, tag in tagged_tokens:
        wordnet_tag = map_postag_into_wordnet(tag)
        lemma = lemmatizer.lemmatize(word, pos=wordnet_tag)
        lemma_list.append(lemma)

    # Removing stopwords and punctuation
    stopwords_verbs = ['say', 'get', 'go', 'know', 'may', 'need', 'like', 'make', 'see', 'want', 'come', 'take', 'use',
                       'would', 'can']
    stopwords_other = ['one', 'mr', 'bbc', 'image', 'getty', 'de', 'en', 'caption', 'also', 'copyright', 'something']
    stop_words = stopwords.words("english") + stopwords_verbs + stopwords_other
    filtered_lemma_list = []
    for word in lemma_list:
        if word not in stop_words:
            if word.isalpha() and len(word) > 3:
                filtered_lemma_list.append(word)

    return filtered_lemma_list


def map_postag_into_wordnet(postag):
    # input: value from pos_tag
    # output: value for WordNet lemmatizer
    # mapping logic:
    #   pos_tags that begin with J are adjectives
    #                       with V are verbs
    #                       with N are nouns
    #                       with R are adverbs
    #
    # Create a dictionary with the mapping:
    tag_map = {"j": wordnet.ADJ,
               "n": wordnet.NOUN,
               "v": wordnet.VERB,
               "r": wordnet.ADV}
    # Create a default option, to be used when the mapping fails:
    default_pos = wordnet.NOUN
    # Now return the value for the appropriate key (key = 1st letter of the postag)
    #   if the key is not found, return the chosen default
    wordnet_tag = tag_map.get(postag[0].lower(), default_pos)
    return wordnet_tag
