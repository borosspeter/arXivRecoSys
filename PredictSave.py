import pandas as pd
from datetime import datetime
from datetime import timedelta
import warnings
import time
import arxiv
import sqlite3
import unidecode
import pickle

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

def progress_bar(relevance):
    s = 100-int(100-100*relevance/5)
    if s > 14:
        if s > 17:
            color = 'red'
        else:
            color = 'orange'
    else:
        color = 'green'
    return '|<font color="'+color+'">'+'█'*s+'</font>'+'-'*(20-s)+'|'

categories = {'cond-mat', 'cond-mat.mes-hall', 'quant-ph', 'cond-mat.supr-con', 'cond-mat.mtrl-sci', 'cond-mat.str-el', 'cond-mat.other'}

output = ['html'] # 'html' and/or 'db'

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
            lastquery += 1
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

if 'db' in output:

    tosql_df = predicted_df[['id','published','authors_FdotLastcomma','title','abstract','relevance']].rename(columns = {"authors_FdotLastcomma": "authors"})

    conn = sqlite3.connect('data/manuscripts.db')
    c = conn.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS manuscripts (id, published, authors, title, abstract, relevance)')
    conn.commit()
    tosql_df.to_sql('manuscripts', conn, if_exists = 'replace', index = False)

if 'html' in output:

    tohtml_df = predicted_df[['id','published','authors_FdotLastcomma','title','abstract','relevance']].rename(columns = {"authors_FdotLastcomma": "authors"})

    day = False
    html = '<ul>\n'
    html += '<hr>\n'
    for idx, row in tohtml_df[tohtml_df['relevance']>0.5].sort_values(by=['published','relevance'],ascending=False).iterrows():
        if day != row['published']:
            html += '<b><font size="+2">'+row['published'].strftime('%-d %B, %Y')+'</font></b>\n'
            html += '<hr>\n'
            day = row['published']
        html += '<li>\n'
        html += '<a href="'+row['id']+'">arXiv:'+row['id'].split('http://arxiv.org/abs/')[-1][:-2]+'</a>'
        html += '<br />\n'
        html += '<b><font size="+1">Relevance:</b></font>'
        html += '<font size="+0" style="font-family:courier, monospace">'+progress_bar(row['relevance'])+'</font>'
        html += '<font size="+1">'+str(round(100*row['relevance'],1))+'%</font>'
        html += '<br />\n'
        html += '<b><font size="+1">Title:</b> '+row['title']+'</font>'
        html += '<br />\n'
        html += '<b><font size="+1">Authors:</font></b> <i>'+row['authors']+'</i>'
        html += '<br />\n'
        html += '<b><font size="+1">Abstract:</font></b> '+row['abstract']
        #html += '<br />\n'
        #html += '<b>Submitted:</b> '+row['published'].strftime('%-d %B, %Y')+'\n'
        html += '<br />\n'
        html += '</li>\n'
        html += '<hr>\n'
    html += '</ul>'

    with open("data/manuscripts.html", "w") as file:
        file.write(html)