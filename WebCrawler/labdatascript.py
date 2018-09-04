#import textanalysis.py as ta
import pyLDAvis
import pandas as pd
import pymysql.cursors
from pandas import DataFrame
import pyperclip
import nltk
import spacy
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import difflib
import Levenshtein
import fuzzywuzzy
from fuzzywuzzy import fuzz
import re # Regex Package
from string import punctuation # Punctuation removal package
import requests # Web Request Package
from bs4 import BeautifulSoup # Formatting the web html package
import nltk # Text toolkit package
from nltk.corpus import stopwords # Stopwords Removal package
from nltk.tag import StanfordNERTagger # Stanford NER tagger package
from nltk import SnowballStemmer

from collections import Counter # Iteration package
import matplotlib.pyplot as plt # Plotting package
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS # Wordcloud package
import gensim # Topic Modelling Package
from nltk.tokenize import word_tokenize # Sentence tokenizer package
from gensim.models.coherencemodel import CoherenceModel # Topic Modelling package
import gensim # Topic Modelling Package
import gensim.corpora as corpora # Topic Modelling package
from gensim.utils import simple_preprocess # Topic Modelling package
from gensim.models import CoherenceModel # Topic Modelling package
from nltk.collocations import BigramCollocationFinder # Word Collaction finder
from nltk.collocations import TrigramCollocationFinder # Word Collaction finder
from nltk.collocations import QuadgramCollocationFinder
import pyLDAvis.gensim
from nltk.metrics.association import QuadgramAssocMeasures
import collections
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy as np
from collections import Counter, OrderedDict
from sklearn.decomposition import LatentDirichletAllocation
import random


stop_words = stopwords.words('english') # English Stopwords removal


# <---------- Functions, functions, functions ---------->


def clean_corpus(corpus):
    #get rid of the punctuations and set all characters to lowercase
    RE_PREPROCESS = r'\W+|\d+' #the regular expressions that matches all non-characters

    processed_corpus = np.array( [ re.sub(RE_PREPROCESS, ' ', comment) for comment in corpus] )

    nltk.download('stopwords') #download the latest stopwords
    eng_stopwords = stopwords.words('english')

    processed_bag_of_words, processed_features = create_bag_of_words(corpus, stop_words=eng_stopwords)
    dict_processed_word_counts = get_word_counts(processed_bag_of_words, processed_features)

    top_10_words = list(dict_processed_word_counts.keys())[:15]
    domain_specific_stopwords = eng_stopwords + top_10_words
    processed_bag_of_words, processed_features = create_bag_of_words(processed_corpus,
                                                                 stop_words=domain_specific_stopwords,
                                                                 stem=True,
                                                                 USE_IDF=True)
#    dict_processed_word_counts = get_word_counts(processed_bag_of_words, processed_features)
    return processed_bag_of_words, processed_features, domain_specific_stopwords



def create_bag_of_words(corpus,
                       NGRAM_RANGE=(0,1),
                       stop_words = None,
                        stem = False,
                       MIN_DF = 0.0,
                       MAX_DF = 1.0,
                       USE_IDF=False):

    # corpus = []
    # for row in column:
    #     if not(row is None):
    #         corpus.append(row)

    ANALYZER = "word" #unit of features are single words rather then phrases of words
    STRIP_ACCENTS = 'unicode'
    stemmer = nltk.SnowballStemmer("english")

    if stem:
        tokenize = lambda x: [stemmer.stem(i) for i in x.split()]
    else:
        tokenize = None
    vectorizer = CountVectorizer(analyzer=ANALYZER,
                                tokenizer=tokenize,
                                ngram_range=NGRAM_RANGE,
                                stop_words = stop_words,
                                strip_accents=STRIP_ACCENTS,
                                min_df = MIN_DF,
                                max_df = MAX_DF)
    bag_of_words = vectorizer.fit_transform( corpus ) #transform our corpus is a bag of words
    features = vectorizer.get_feature_names()

    if USE_IDF:
        NORM = None #turn on normalization flag
        SMOOTH_IDF = True #prvents division by zero errors
        SUBLINEAR_IDF = True #replace TF with 1 + log(TF)
        transformer = TfidfTransformer(norm = NORM,smooth_idf = SMOOTH_IDF,sublinear_tf = True)
        #get the bag-of-words from the vectorizer and
        #then use TFIDF to limit the tokens found throughout the text
        tfidf = transformer.fit_transform(bag_of_words)

        return tfidf, features
    else:
        return bag_of_words, features


#not mine
def get_word_counts(bag_of_words, feature_names):
    """
    Get the ordered word counts from a bag_of_words

    Parameters
    ----------
    bag_of_words: obj
        scipy sparse matrix from CounterVectorizer
    feature_names: ls
        list of words

    Returns
    -------
    word_counts: dict
        Dictionary of word counts
    """
    np_bag_of_words = bag_of_words.toarray()
    word_count = np.sum(np_bag_of_words,axis=0)
    np_word_count = np.asarray(word_count).ravel()
    dict_word_counts = dict( zip(feature_names, np_word_count) )

    orddict_word_counts = OrderedDict(
                                    sorted(dict_word_counts.items(), key=lambda x: x[1], reverse=True), )

    return orddict_word_counts

#not mine
def create_topics(tfidf, features, N_TOPICS=3, N_TOP_WORDS=5,):
    """
    Given a matrix of features of text data generate topics

    Parameters
    -----------
    tfidf: scipy sparse matrix
        sparse matrix of text features
    N_TOPICS: int
        number of topics (default 10)
    N_TOP_WORDS: int
        number of top words to display in each topic (default 10)

    Returns
    -------
    ls_keywords: ls
        list of keywords for each topics
    doctopic: array
        numpy array with percentages of topic that fit each category
    N_TOPICS: int
        number of assumed topics
    N_TOP_WORDS: int
        Number of top words in a given topic.
    """

    #with progressbar.ProgressBar(maxval=progressbar.UnknownLength) as bar:
    lda = LatentDirichletAllocation( n_topics= N_TOPICS,
                                   learning_method='online') #create an object that will create 5 topics

    doctopic = lda.fit_transform( tfidf )


    ls_keywords = []
    res = []
    for i, topic in enumerate(lda.components_):
        word_idx = np.argsort(topic)[::-1][:N_TOP_WORDS]
        keywords = ', '.join( features[i] for i in word_idx)
        ls_keywords.append(keywords)
#        print(i, keywords)
        i+=1
        res.append((i, keywords))

    return ls_keywords, doctopic, res




def ie_preprocess(document, pos_sequence): # entity tagging / chunking
    sentences = nltk.sent_tokenize(document)

    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    cp = nltk.RegexpParser('CHUNK: ' + pos_sequence)
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    for sent in sentences:
        print(nltk.ne_chunk(sent, binary=True))
        tree = cp.parse(sent)
        for subtree in tree.subtrees():
            if subtree.label() == 'CHUNK': print(subtree)
