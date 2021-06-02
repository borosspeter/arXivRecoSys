import pandas as pd
from datetime import datetime
from datetime import timedelta
import warnings
import time
import arxiv
import sqlite3
import unidecode
import pickle
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB

def get_authors_FLast_arxivapi(authors):
    r = []
    for authorv in authors:
        author = authorv.split(' ')
        r.append(unidecode.unidecode(author[0][0]+author[-1]))    
    return ' '.join(r)

def get_authors_FdotLastcomma(authors):
    r = []
    for author in authors:
        authorv = author.split(' ')
        r.append(unidecode.unidecode(' '.join([x[0]+'.' for x in authorv[0:-1]])+' '+authorv[-1]))
    return ', '.join(r)

categories = {'cond-mat', 'cond-mat.mes-hall', 'quant-ph', 'cond-mat.supr-con', 'cond-mat.mtrl-sci', 'cond-mat.str-el', 'cond-mat.other'}

filename = 'data/model.sav'
pipeline = pickle.load(open(filename, 'rb'))

days = 1
delta = timedelta(days = days)
catstr = '+OR+'.join(['cat:'+x for x in categories])
client = arxiv.Client()
nquery = 500
startquery = 0
lastquery = nquery
latestdate = False
predicted_df = pd.DataFrame(columns = ['id','published','authors_FdotLastcomma','authors_FLast', 'title', 'abstract'])

while lastquery == nquery:
    feedparser = client._parse_feed(url='http://export.arxiv.org/api/query?search_query='+catstr+'&start='+str(startquery)+'&max_results='+str(nquery)+'&sortBy=submittedDate')
    if len(feedparser.entries) == 0:
        warnings.warn("Warning...........arXiv api provides 0 entry")
    lastquery = 0
    for entry in feedparser.entries:
        if not(latestdate): latestdate = datetime.strptime(entry.published[0:10],'%Y-%m-%d')
        if latestdate - datetime.strptime(entry.published[0:10],'%Y-%m-%d') < delta:
            lastquery+=1
            predicted_df = predicted_df.append({
                'id' : entry.id,
                'authors_FdotLastcomma' : get_authors_FdotLastcomma([author['name'] for author in entry.authors]),
                'authors_FLast' : get_authors_FLast_arxivapi([author['name'] for author in entry.authors]),
                'title' : entry.title.rstrip(),
                'abstract' : entry.summary.rstrip(),
                'published': datetime.strptime(entry.published[0:10],'%Y-%m-%d')
                            }, ignore_index = True)
    startquery += nquery
    time.sleep(5)

Xnew = predicted_df[['authors_FLast','title','abstract']]

predicted_df['relevance'] = [x[1] for x in pipeline.predict_proba(Xnew)]

conn = sqlite3.connect('data/manuscripts.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS manuscripts (id, published, authors, title, abstract, relevance)')
conn.commit()

tosql_df = predicted_df[['id','published','authors_FdotLastcomma','title','abstract','relevance']]

tosql_df.to_sql('manuscripts', conn, if_exists='replace', index = False)