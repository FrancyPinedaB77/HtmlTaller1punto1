from django.db import models
import xmltodict
import paramiko

# Create your models here.

def run(command):
    print(command)
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('????', username='????', password='????')
        stdin, stdout, stderr = ssh.exec_command(command)
        return(stdout.read())
    finally:
        ssh.close()
    
class News(object):
    def __init__(self, code, title, date, url):
        self.code = int(code)
        self.title = title
        self.date = date
        self.url = url

class NewsReader(object):
    def __init__(self, path):
        xml = run("cat " + path)
        doc = xmltodict.parse(xml)
    
        self.news = []
        for item in doc['resultados']['item']:
            myNews = News(item['id'], item['titulo'], item['fecha'], item['link'])
            self.news.append(myNews)

    def filter(self, string, kind):
        ids = run("python filter.py \"{}\" {}".format(string, kind))
        print(ids.split(b'\n'))
        ids = [int(x) for x in ids.split(b'\n')[:-1]]
        filtered = []
        for news in self.news:
            if news.code in ids:
                filtered.append(news)
        return filtered
