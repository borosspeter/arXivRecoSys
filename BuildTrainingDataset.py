import numpy as np
import pandas as pd
from datetime import datetime
from datetime import timedelta
import json
import arxiv
import urllib.request as libreq
import re
from collections import Counter
import unidecode
import itertools
import pickle

def get_authors_LastF(authors):
    r = []
    for author in authors:
        if len(author[1]) == 0: r.append(unidecode.unidecode(author[0]))
        else: r.append(unidecode.unidecode(author[0]+author[1][0]))    
    return ' '.join(r)

categories = {'cond-mat', 'cond-mat.mes-hall', 'quant-ph', 'cond-mat.supr-con', 'cond-mat.mtrl-sci', 'cond-mat.str-el', 'cond-mat.other'}

articles = []

with open("data/arxiv-metadata-oai-snapshot.json", "r") as f:
    for l in f:
        d = json.loads(l)
        if categories & set(d['categories'].split(' ')):
            d['authors_LastF'] = get_authors_LastF(d['authors_parsed'])
            articles.append(d)

articles_df = pd.DataFrame().from_records(articles)

authors = ['BorossP','OroszlanyL','PalyiA','AsbothJ','SzechenyiG']

ids = list(articles_df[articles_df["authors_LastF"].str.contains('|'.join(authors))]['id'])

refs=[]

for id in ids:
    with libreq.urlopen('https://www.prophy.science/api/arxiv/' + id) as url:
        refs1paper = json.loads(url.read())
    refs.extend([ref['arxivId'] for ref in refs1paper['references'] if ref['arxivId'] != None])

refscounted = sorted(Counter(refs).items(), key=lambda pair: pair[1], reverse=True)
refs = [entry[0] for entry in refscounted]
counts = [entry[1] for entry in refscounted]
refscounteddict = dict(zip(refs, counts))

cited_df = articles_df[articles_df['id'].isin(refs)][['abstract','title','authors_LastF','id']].replace(refscounteddict).rename(columns = {'id': 'citation', 'authors_LastF': 'authors'})
cited_df['cited'] = True

notcited_df = articles_df[articles_df['id'].isin(refs) == False][['abstract','title','authors_LastF']].sample(n = 10*len(cited_df)).rename(columns = {'authors_LastF': 'authors'})
notcited_df['citation'] = 0
notcited_df['cited'] = False

all_df = pd.concat([cited_df, notcited_df])

all_df.to_csv('data/all_df.csv')