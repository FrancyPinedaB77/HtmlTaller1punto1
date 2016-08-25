import requests
import re, datetime
from threading import Thread

TIMEOUT = 10

def timestamp():
    return '[{}]'.format(datetime.datetime.utcnow())

def get_url(url, try_hard=False):
    print(timestamp(), 'Trying to get', url)
    try:
        if try_hard:
            response = requests.get(url, timeout = TIMEOUT).text
        else:
            response = requests.get(url).text
        response[0]
        print(timestamp(), 'Succesfully got', url)
        return response
    except:
        print(timestamp(), 'Error: Couldn\'t get', url)

class Unit(object):
    def __init__(self, name, url, webpage):
        self.name = name
        self.url = url
        self.webpage = webpage
        self.links = []
        self.concat_links = ''

    def get_calendar(self):
        match = re.findall('(https?://.+/)(cat|day|month|year)([\._](listevents|calendar))', self.concat_links)
        if len(match) > 0:
            return match[0][0]+'year'+match[0][2]+'/'
        match = re.findall('(https?://.+task=)(year|month|day)\.listevents', self.concat_links)
        if len(match) > 0:
            return match[0][0]+'year.listevents'
        return None

    def get_basic(self):
        match = re.findall('(.*[^/]/[^/]*([Ee]ventos?(\.aspx|/|-futuros)?))', self.concat_links)
        if len(match) > 0:
            return match[0][0]
        return None

    def fix_relative(self, url):
        if 'http' in url:
            return url
        return self.url + url

    def get_links(self):
        self.links = re.findall('href=["\']([^\'"]*([Ee]ventos?|noticias|icagenda|icalrepeat|listevents)[^\'"]*)["\']', self.webpage)
        self.links = [self.fix_relative(i[0]) for i in self.links]
        clean_links = []
        for link in self.links:
            if ('eventos.uniandes' not in link) and ('uniandes' in link):
                clean_links.append(link)
        self.links = clean_links
        if len(self.links) == 0:
            print(timestamp(), 'Error: {} unit didn\'t found any links'.format(self))
        else:
            self.links.sort(key=lambda i: len(i))
            self.concat_links = '\n'.join(self.links)

    def get_events_link(self):
        self.get_links()
        calendar = self.get_calendar()
        basic = self.get_basic()
        if calendar:
            print(timestamp(), '{} unit found links to events at {}'.format(self, calendar))
            return calendar
        elif basic:
            print(timestamp(), '{} unit found links to events at {}'.format(self, basic))
            return basic
        else:
            for link in self.links:
                print(timestamp(), '{} unit found possible candidate {}'.format(self, link))
    
    def __str__(self):
        return(self.name)
           
class Spidy(object):
    def __init__(self, root_url):
        self.root_url = root_url
        self.root_page = get_url(self.root_url, try_hard=True)
        self.units = []
        
    def get_units(self):
        matches = re.findall('<li><a\s+href="https?://([^"]+uniandes\.edu\.co)[^"]*"\s+[^>]*>([^<]*(Facultad|Centro|Escuela|Departamento)[^<]*)</a></li>', self.root_page)
        matches = list(set([i[:2] for i in matches]))
        matches.sort(key=lambda i: i[1])

        names = []
        urls = []
        pages = []
        threads = []
        
        for match in matches:
            urls.append('http://'+match[0])
            names.append(match[1])
            pages.append(None)
            threads.append(None)

        def f(i, pages):
            pages[i] = get_url(urls[i], try_hard=True)
            match = re.findall('location.href="(https?://[^"]+)"', pages[i])
            if len(match) > 0:
                print(timestamp(), 'Found redirection from {} to {}'.format(urls[i], match[0]))
                urls[i] = match[0]
                pages[i] = get_url(urls[i], try_hard=True)

        for i in range(len(threads)):
            threads[i] = Thread(target=f, args=(i, pages))
            threads[i].start()

        for thread in threads:
            thread.join()

        for name, url, page in zip(names, urls, pages):
            if page:
                self.units.append(Unit(name, url, page))
                
    def get_all_links(self):
        for unit in self.units:
            unit.get_events_link()

my_spidy = Spidy('http://uniandes.edu.co/institucional/facultades/facultades')
my_spidy.get_units()
my_spidy.get_all_links()
