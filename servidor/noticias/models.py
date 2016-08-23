import subprocess, xmltodict
from os.path import realpath
from django.db import models

def run(command):
    subp = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = subp.communicate()
    return(out)

PATH = realpath('./bin')
XQUERY = 'sh {}/busqueda.sh'.format(PATH) + ' -i -o {} {}'

class News(object):
    def __init__(self, code, title, date, url, description):
        self.code = int(code)
        self.title = title
        self.date = date
        self.url = url
        self.description = description

class NewsReader(object):
    def __init__(self):
        self.get_news()
        
    def get_news(self):
        doc = xmltodict.parse(open('{}/db_feed.xml'.format(PATH),'r').read())
        self.news = []
        for feed in doc['resultados']['feed']:
            for item in feed['item']:
                myNews = News(item['id'], item['title'], item['pubDate'], item['link'], item['description'])
                self.news.append(myNews)
        
    def filter_xquery(self, string, kind):
        ids = run(XQUERY.format(kind, string))
        ids = [int(x) for x in ids.split(b'\n')[:-1]]
        filtered = []
        for news in self.news:
            if news.code in ids:
                filtered.append(news)
        return filtered

