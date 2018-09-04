from nltk.tag import StanfordNERTagger
from nltk.internals import find_jars_within_path
import labdatascript as lb
import re
import unicodedata
from sner import Ner
from nltk import tokenize

st = Ner(host='localhost',port=9199) #7-class
# stanford_dir = st._stanford_jar.rpartition('/')[0] #these lines are just a hack to get around the java problem
# from nltk.internals import find_jars_within_path
# stanford_jars = find_jars_within_path(stanford_dir)
# st._stanford_jar = ':'.join(stanford_jars)


def analyze_texts(dict, top_num=5): #takes soups_dict of texts gathered, creates corpus

    '''
    Draws from labdatascript functions for NLP analysis of gathered texts

    Input: result dictionary from web crawler with gathered text as values, top n to slice from analysis results

    Output: dict with wordcounts, bi + tri + quad grams, topic model

    Further: takes top x values from ngrams, passed in as parameter in function call
    '''
    corpus = []
    for i in dict.values():
        i = re.sub('[0-9]+', '', i)
        corpus.append(i)

    processed_bow, processed_feats, domain_specific_stopwords = lb.clean_corpus(corpus)
    word_counts = lb.get_word_counts(processed_bow, processed_feats)
    keys, topics, out = lb.create_topics(processed_bow, processed_feats)
    bigrambow, bigramfeats = lb.create_bag_of_words(corpus, stop_words=domain_specific_stopwords, NGRAM_RANGE=(2,2))
    bigramcount = lb.get_word_counts(bigrambow, bigramfeats)
    trigrambow, trigramfeats = lb.create_bag_of_words(corpus, stop_words=domain_specific_stopwords, NGRAM_RANGE=(3,3))
    trigramcount = lb.get_word_counts(trigrambow, trigramfeats)
    quadgrambow, quadgramfeats = lb.create_bag_of_words(corpus, stop_words=domain_specific_stopwords, NGRAM_RANGE=(4,4))
    quadgramcount = lb.get_word_counts(quadgrambow, quadgramfeats)
#    report_analysis(word_counts, res, bigramcount, trigramcount, quadgramcount)
    result_dict = {}
    int_top_num = int(top_num)
    count_items = list(word_counts.items())[:int_top_num]
    result_dict['counts'] = count_items
    result_dict['topics'] = topics
    bigram_items = list(bigramcount.items())[:int_top_num]
    result_dict['bigrams'] = bigram_items
    trigram_items = list(trigramcount.items())[:int_top_num]
    result_dict['trigrams'] = trigram_items
    quadgram_items = list(quadgramcount.items())[:int_top_num]
    result_dict['quadgrams'] = quadgram_items
    return result_dict



def filter_by_keyword(corp, keyword): #filters sentences based on keyword (i.e. PERSON, LOCATION, MONEY, ORGANIC)
    my_set = set()
#    sentences = corp.split('.')
    sentences = tokenize.sent_tokenize(corp)


    for sent in sentences:
#        s = sent.split()
        tagged = st.get_entities(sent) #this is where it's slow: it's only processing about 1 sentence per second
#        print(tagged)
        for n,i in tagged:
            if i == keyword:
                my_str = unicodedata.normalize("NFKD", sent)
                my_set.add(my_str)
    return my_set
