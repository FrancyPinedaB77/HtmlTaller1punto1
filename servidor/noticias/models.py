from django.db import models
import xmltodict
import paramiko

# Create your models here.

GETNEWS = "cat data_full.xml"
SEARCH = "python filter.py \"{}\" {}"

WORKER = '????'
USER = '????'
PASS = '????'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(WORKER, username=USER, password=PASS)

def run(command):
    print("Running over ssh:", command)
    stdin, stdout, stderr = ssh.exec_command(command)
    return(stdout.read())
    
class News(object):
    def __init__(self, code, title, date, url):
        self.code = int(code)
        self.title = title
        self.date = date
        self.url = url

class NewsReader(object):
    def __init__(self, path):
        xml = run(GETNEWS)
        doc = xmltodict.parse(xml)
        self.news = []
        for feed in doc['resultados']['feed']:
            for item in feed['item']:
                myNews = News(item['id'], item['titulo'], item['fecha'], item['link'])
                self.news.append(myNews)

    def filter(self, string, kind):
        ids = run(SEARCH.format(kind, string))
        ids = [int(x) for x in ids.split(b'\n')[:-1]]
        filtered = []
        for news in self.news:
            if news.code in ids:
                filtered.append(news)
        return filtered
