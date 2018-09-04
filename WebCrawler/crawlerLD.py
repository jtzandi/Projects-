import re
import utilv2 as util
import helperfuncs as hfunc
import analysisfuncs as anfunc
import bs4
import queue
import json
import sys
import csv
import urllib
from lxml import html
import requests
from urllib.parse import urlparse
import pandas as pd
from bs4.element import Comment
import labdatascript as lb
import nltk
from nltk.corpus import stopwords
import numpy as np
import json
from collections import OrderedDict
import timeit
import os
import re
import glob
from pathlib import Path
import pickle


INDEX_IGNORE = set(['a', 'also', 'an', 'and', 'are', 'as', 'at', 'be',
                    'but', 'by', 'course', 'for', 'from', 'how', 'i',
                    'ii', 'iii', 'in', 'include', 'is', 'not', 'of',
                    'on', 'or', 's', 'sequence', 'so', 'social', 'students',
                    'such', 'that', 'the', 'their', 'this', 'through', 'to',
                    'topics', 'units', 'we', 'were', 'which', 'will', 'with',
                    'yet'])

nltk.download('stopwords') #download the latest stopwords
eng_stopwords = stopwords.words('english')

soups_dict = {}


def collect_start_urls(excel_file_path, col_name):
    '''
    Basic helper function for grabbing all non-None items in excel column

    Input: excel file path, name of column to extract

    Output: list of starting urls
    '''
    # start_list = []
    df = pd.read_excel(io=excel_file_path)
    data = df[col_name]
    for row in data:
        if not (row is None):
            start_list.append(str(row))
    return start_list




def get_soup(url, temp_dict): #grabs text from 'p' tags only
    '''
    Helper function to get a bs4.BeautifulSoup from a given url.
    Converts the url to an acceptable format to check util.is_url_ok_to_follow(url, limiting_domain)

    Input: (url)

    Output:
        url: updated url extracted from request
        soup: (bs4.BeautifulSoup) from url
    '''
    url = util.remove_fragment(url)
    request = util.get_request(url)
    url = util.get_request_url(request)
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    texts = soup.findAll('p',text=True)
    res = ' '.join(x.text for x in texts)
    soups_dict[url] = res
    temp_dict[url] = res
    return url, soup


def put_links(soup, url, limiting_domain, q, lst, my_list, num_pages_to_crawl_each):
    '''
    Updates existing queue and list with links found on the url.
    The list keeps track of links added; the queue keeps track of links to be opened.

    Inputs:
        soup: (bs4.BeautifulSoup) soup of the starting_url orthe url that was
            taken out from the queue
        url: either the starting_url or an url that was taken out from the queue
        limiting_domain: domain name
        q: (queue) containing links that were have been added in in prior steps
        lst: (list) containing all the links added in the prior steps

    Outputs: None
    '''

    links = soup.find_all("a",href=True)
    links = [link['href'] for link in links]
    links = filter(None, links)
    links = list(links)
    converted_links = []
    for link in links:
        link = util.convert_if_relative_url(url, link)
        link = util.remove_fragment(link)
        converted_links.append(link)

        if link not in lst and util.is_url_ok_to_follow(link, limiting_domain) and len(my_list) < num_pages_to_crawl_each:
                #print('Link is ok to follow')
                q.put(link)
                lst.append(link)
                my_list.append(link)



def get_urls(num_pages_to_crawl_each): #main function

    '''
    Main Function: Crawls the web from each start url a specified number of links and collects p-tag text from all

    Input: number of pages to crawl from each start link

    Output: (global) dict pairing links with text + list of all urls visited and chain of pages that tracks association of links
    '''

    starting_urls = ['https://gspp.berkeley.edu/programs/masters-of-public-policy-mpp/tuition-and-financial-aid/gspp-departmental-fellowships',
    'https://gspp.berkeley.edu/programs/masters-of-public-policy-mpp/tuition-and-financial-aid/gspp-departmental-fellowships',
    'https://gspp.berkeley.edu/programs/ppia-junior-summer-institute',
    'https://www.cbcfinc.org/fellowships/']


    # starting_urls = ['https://gspp.berkeley.edu/programs/masters-of-public-policy-mpp/tuition-and-financial-aid/gspp-departmental-fellowships',
    # 'https://gspp.berkeley.edu/programs/masters-of-public-policy-mpp/tuition-and-financial-aid/gspp-departmental-fellowships',
    # 'https://gspp.berkeley.edu/programs/ppia-junior-summer-institute',
    # 'https://www.cbcfinc.org/fellowships/',
    # 'https://culturalvistas.org/muskie/',
    # 'https://www.rangelprogram.org/',
    # 'https://woodrow.org/fellowships/pickering/',
    # 'https://mcfscholarsprogram.berkeley.edu/',
    # 'https://mcfscholarsprogram.berkeley.edu/',
    # 'https://geediting.com/about/scholarship-program/',
    # 'https://www.ssrc.org/programs/view/abe-fellowship-program/',
    # 'http://www.akdn.org/our-agencies/aga-khan-foundation/international-scholarship-programme',
    # 'https://www.aephi.org/foundation/scholarships/',
    # 'https://www.aauw.org/what-we-do/educational-funding-and-awards/international-fellowships/',
    # 'http://www.acb.org/scholarship',
    # 'http://www.americancouncils.org.ua/en/pages/22/',
    # 'https://www.afb.org/info/afb-2018-scholarship-application/5',
    # 'https://collegefund.org/student-resources/scholarships/scholarship-programs/',
    # 'https://www.aigcs.org/aigc-scholarship-fellowship-opportunities',
    # 'http://www.ampolinstitute.org/index2.html',
    # 'http://www.ajhs.org/academic-awards',
    # 'http://www.amscan.org/fellowships-and-grants/fellowships-and-grants-for-advanced-study-or-research-in-the-usa/',
    # 'https://www.borenawards.org/fellowships/boren-fellowship-basics',
    # 'https://www.bie.edu/ParentsStudents/Grants/index.htm',
    # 'https://www.bushfoundation.org/fellowships/bush-fellowship',
    # 'https://foundation.caionline.org/scholarships/hanke/',
    # 'http://www.cfuw.org/en-ca/fellowshipsawards.aspx',
    # 'http://thecirifoundation.org/scholarships/',
    # 'https://chci.org/',
    # 'https://www.doe.k12.de.us/Page/996',
    # 'http://www.paynefellows.org/?areaid=2&contentid=941&CFID=705&CFTOKEN=DD846249-CFBC-458C-855D102DD55C8BC2',
    # 'https://www.eastwestcenter.org/education/student-programs/scholarships-and-fellowships/united-states-south-pacific-scholarship',
    # 'http://www.hluce.org/publicpolicy.aspx']


    if os.path.exists('results/'): #directory for storing outcome of script
        pass
    else:
        os.mkdir('results/')
    url_lst = []
    q = queue.Queue()
    count = 1

    for starting_url in starting_urls:
        temp_dict = {}
        my_list = []
        limiting_domain = urlparse(starting_url).netloc #comment this out if no limiting domain
        try:
            starting_url, soup = get_soup(starting_url, temp_dict)
            put_links(soup, starting_url, limiting_domain, q, url_lst, my_list, num_pages_to_crawl_each)

            while not q.empty():
                new_url = q.get()
                limiting_domain = urlparse(new_url).netloc
                new_url, soup = get_soup(new_url, temp_dict)
                put_links(soup, new_url, limiting_domain, q, url_lst, my_list, num_pages_to_crawl_each)


        except Exception as e:
            print('In get_urls function: ' + str(e))

        pth = 'results' + '/' + str(limiting_domain)
        print(pth)
        start = str('results' + str(count)) + '.t' #the 'results' part of this can be changed to change the write-to name of files
                    #DO NOT change the .t concatentation, otherwise acces_analyze_files will return nothing
        hfunc.pickle_data(temp_dict,pth, start) #add .t as filetype to mark as text
        count += 1
    hfunc.pickle_data(soups_dict, 'results/all_results', 'all.t')
    return url_lst


def access_analyze_files(): #used for accessing all gathered text (from crawler), analyzing, then writing the analysis.
    for filename in glob.iglob('results/**/*.t', recursive=True): #DO NOT change the .t search, otherwise will return nothing
        if not(os.path.isdir(filename)):
            txt_dict = hfunc.unpickle_data(filename)
            res = anfunc.analyze_texts(txt_dict, 10)
            new = filename[:-2]
            new_path = Path(str(new) + 'analysis').absolute()
            my_file = open(new_path, 'wb')
            pickle.dump(input, my_file)
            my_file.close()


list_result = get_urls(5) #RUNS webcrawler (or not, if commented out)



some = hfunc.unpickle_data('results/gspp.berkeley.edu/results1.t')
all = hfunc.unpickle_data('results/all_results/all.t')
#some_of_this = anfunc.analyze_texts(some)



#access_analyze_files()    #analyzes all text files and writes results as pickled dictionary



corp = hfunc.get_corpus(all) #creates a corpus from gathered text

stuff = anfunc.filter_by_keyword(corp, 'ORGANIZATION') #filters sentences from corpus based on keyword (see function in analysisfuncs for list of keywords)
print(stuff)
