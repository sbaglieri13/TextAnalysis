from nltk import tokenize
from nltk import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.corpus import stopwords


def preprocessing_en(text):
    # Word tokenization
    tokenizer = tokenize.TreebankWordTokenizer()
    tokens = tokenizer.tokenize(text.lower())

    # print("Text tokenize: ", tokens)

    # Normalization
    lemmatizer = WordNetLemmatizer()
    tagged_tokens = pos_tag(tokens)
    lemma_list = []
    for word, tag in tagged_tokens:
        wrdnt_tag = map_postag_into_wordnet(tag)
        lemma = lemmatizer.lemmatize(word, pos=wrdnt_tag)
        lemma_list.append(lemma)

    # print("Text lemmatizer: ", lemma_list)

    # Removing stopwords and punctuation
    stop_words = stopwords.words("english")
    filtered_lemma_list = []
    for word in lemma_list:
        if word not in stop_words:
            if word.isalpha():
                filtered_lemma_list.append(word)

    # print("Text stopwords: ", filtered_lemma_list)

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
    wrdnt_tag = tag_map.get(postag[0].lower(), default_pos)
    return wrdnt_tag