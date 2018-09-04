import pickle
import os
import unicodedata
from pathlib import Path
import re

def tag_visible(element):
    '''
    don't worry about it -- just for use in commented out function for grabbing visible text
    '''
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def get_corpus(dict):
    '''
    Helper function for stringifying all text (values) from resulting dict of links and texts

    Input: dictionary

    output: string of all combined text gathered
    '''

    lst = []
    for i in dict.values():
        i = re.sub('[0-9]+', '', i)
        lst.append(i)
    out = ''.join(lst)
    return out


# def reencode(ngram): #ignore for now
#     '''
#     Don't worry about this -- just needed to fix a Python problem with going from int64 to json.dumps
#     '''
#     nlist = []
#     vals = ngram.items()
#     for val in vals:
#         nlist.append((val[0], int(val[1])))
#     od = OrderedDict(nlist)
#     return od



def pickle_data(input, pth, url): #creates directory based on limiting domain and pickles input to file
    path = Path(pth).absolute()
#    print(path)
    if Path.exists(path):
        pass
    else:
        Path.mkdir(path)
    new_path = Path(str(path) + '/' + str(url)).absolute()
    my_file = open(new_path, 'wb')
    pickle.dump(input, my_file)
    my_file.close()

def unpickle_data(path): #loads pickled data from file in directory
    my_file = open(path, 'rb')
    output = pickle.load(my_file)
    my_file.close()
    return output

def make_df(dict, *cols): #makes a dataframe
    df = pd.DataFrame(list(dict.items()), columns=[*cols])
    return df
