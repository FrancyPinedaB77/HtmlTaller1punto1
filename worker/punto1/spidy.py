from urllib import request
import re, datetime

TIMEOUT = 1000

def timestamp():
    return '[{}]'.format(datetime.datetime.utcnow())

def get_url(url, try_hard=False):
    print(timestamp(), 'Trying to get', url)
    try:
        if try_hard:
            response = request.urlopen(url, timeout = TIMEOUT)
        else:
            response = request.urlopen(url)
        return response.read().decode()
    except:
        print(timestamp(), 'Error: Couldn\'t get', url)

class Unit(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.webpage = get_url(self.url, try_hard=True)
        self.links = []
        self.concat_links = ''

    def get_calendar(self):
        match = re.findall('(http://.+/)(cat|day|month|year)\.(listevents|calendar)', self.concat_links)
        if len(match) > 0:
            return match[0][0]+'year.'+match[0][2]+'/'
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
        if len(self.links) == 0:
            print(timestamp(), 'Error: {} unit didn\'t found any links'.format(self))
        else:
            self.links.sort(key=lambda i: len(i[0]))
            self.links = [self.fix_relative(i[0]) for i in self.links]
            self.concat_links = '\n'.join(self.links)

    def get_events_link(self):
        calendar = self.get_calendar()
        basic = self.get_basic()
        if calendar:
            print(timestamp(), '{} unit found links to events at {}'.format(self, calendar))
            return calendar
        elif basic:
            print(timestamp(), '{} unit found links to events at {}'.format(self, basic))
            return basic
        else:
            print(timestamp(), 'Error: {} unit did not found events link'.format(self))
    
    def __str__(self):
        return(self.name)
           
class Spidy(object):
    def __init__(self, root_url):
        self.root_url = root_url
        self.root_page = get_url(self.root_url, try_hard=True)
        self.units = []
        
    def get_units(self):
        units = re.findall('<li><a\s+href="https?://([^"]+uniandes\.edu\.co)[^"]*"\s+[^>]*>([^<]*(Facultad|Centro|Escuela|Departamento)[^<]*)</a></li>', self.root_page)
        units = list(set([i[:2] for i in units]))
        units.sort(key=lambda i: i[1])
        self.units = [Unit(name, 'http://'+url) for (url, name) in units]

    def get_all_links(self):
        for unit in self.units:
            unit.get_links()
            unit.get_events_link()

my_spidy = Spidy('http://uniandes.edu.co/institucional/facultades/facultades')
my_spidy.get_units()
my_spidy.get_all_links()
