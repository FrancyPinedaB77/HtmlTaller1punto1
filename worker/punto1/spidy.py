import requests, re, datetime, dateparser, json
from threading import Thread
from lxml import html

TIMEOUT = 10
CALENDAR = 'CALENDAR'
BASIC = 'BASIC'
DATE = datetime.datetime.now().strftime('%Y/%m/%d')
PATH = './jsons/'

def timestamp():
    return '[{}]'.format(datetime.datetime.now())

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
        pass

def get_date(info):
    dates = re.findall('\w+,?(\s+(\d{1,2}\s+\w+|\w+\s+\d{1,2}),?\s+\d{4})', info)
    hour = re.findall('^\s*(\d{1,2}:\d{2}[a-z]{0,2})', info,  flags=re.MULTILINE)[0]
    try:
        num_hour = [int(x) for x in hour.split(':')]
        if num_hour[0] < 6:
            hour = '{:02d}:{:02d}'.format(num_hour[0] + 12, num_hour[1])
    except:
        pass
    ans = []
    for date in dates:
        date = date[0]
        day = re.search('(\d{2})[\s,]', date).group(1)
        month = re.search('[a-z]+', date, flags=re.I).group(0)
        year = re.search('(\d{4})', date).group(0)
    
        date = '{} {} {} {}'.format(hour, day, month, year)
        ans.append(dateparser.parse(date))
    return ans[0]

def to_dict(unit):
    dict_unit = unit.__dict__
    del dict_unit['webpage']
    del dict_unit['concat_links']
    del dict_unit['links']
    if unit.events_site:
        dict_events_site = dict_unit['events_site'].__dict__
        del dict_events_site['webpage']
        del dict_events_site['unit']
        dict_events_site['events'] = [x.__dict__ for x in dict_events_site['events']]
        dict_unit['events_site'] = dict_events_site
    return(dict_unit)

class Event(object): 
    def __init__(self, name, url, date):
        self.name = name
        self.url = url
        self.date = date.isoformat()
        
class Events_site(object):
    def __init__(self, url, kind, unit):
        self.url = url
        self.webpage = get_url(self.url, try_hard=True)
        self.kind = kind
        self.unit = unit
        self.events = []
        self.get_events()

    def get_events(self):
        if self.kind == CALENDAR:
            tree = html.fromstring(self.webpage.encode())
            x = tree.xpath('//a[@class="cal_titlelink"]')
            for i in x:
                link = self.unit.fix_relative(i.get('href'))
                i = i.getparent()
                title = i.get('title')
                data_content = i.get('data-content')
                info = re.findall('<[^<>]+>([^<]+)', title)
                if data_content:
                    info += re.findall('<[^<>]+>([^<]+)', data_content)
                info = '\n'.join(info)
                info = re.sub('(Evento único|(Clic para abrir( el evento)?|Click to open event)|(Single event)|(Desde|Hasta|Hora):&nbsp;|((Primer|Último)?( día de un )?[Ee]vento de varios días))', '', info)
                info = re.sub('\s{3,}','\n', info)
                date = get_date(info)
                name = info.split('\n')[0]
                print(timestamp(), "Unit {} found event:".format(self.unit))
                print('\tname {}'.format(name))
                print('\tdate {}'.format(date))
                print('\tlink {}'.format(link))
                self.events.append(Event(name, link, date))
                
class Unit(object):
    def __init__(self, name, url, webpage):
        self.name = name
        self.url = url
        self.webpage = webpage
        self.links = []
        self.concat_links = ''
        self.events_site = None

    def get_calendar(self):
        match = re.findall('(https?://.+/)(cat|day|month|year)([\._](listevents|calendar))', self.concat_links)
        if len(match) > 0:
            return match[0][0]+'month.calendar/{}/-'.format(DATE)
        match = re.findall('(https?://.+task=)(year|month|day)\.listevents', self.concat_links)
        if len(match) > 0:
            return match[0][0]+'mont.calendar/{}/-'.format(DATE)
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
            if ('eventos.uniandes' not in link) and ('uniandes' in link) and ('destacados' not in link):
                clean_links.append(link)
        self.links = clean_links
        if len(self.links) == 0:
            print(timestamp(), 'Error: {} unit didn\'t found any links'.format(self))
            pass
        else:
            self.links.sort(key=lambda i: len(i))
            self.concat_links = '\n'.join(self.links)

    def get_events_link(self):
        self.get_links()
        calendar = self.get_calendar()
        basic = self.get_basic()
        if calendar:
            print(timestamp(), '{} unit found links to events at {}'.format(self, calendar))
            self.events_site = Events_site(calendar, CALENDAR, self)
        elif basic:
            print(timestamp(), '{} unit found links to events at {}'.format(self, basic))
            self.events_site = Events_site(basic, BASIC, self)
        else:
            for link in self.links:
                print(timestamp(), '{} unit found possible candidate {}'.format(self, link))
                pass
        self.to_json()
                
    def to_json(self):
        my_dict = to_dict(self)
        filename = re.search('https?://([^.]+).uniandes.edu.co',self.url).group(1)
        f_output = open(PATH + filename + '.json', 'w')
        f_output.write(json.dumps(my_dict, ensure_ascii=False))
        f_output.close()
        
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
            if pages[i]:
                match = re.findall('location.href="(https?://[^"]+)/"', pages[i])
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
        threads = [None]*len(self.units)

        for i in range(len(self.units)):
            threads[i] = Thread(target=self.units[i].get_events_link)
            threads[i].start()

        for thread in threads:
            thread.join()

my_spidy = Spidy('http://uniandes.edu.co/institucional/facultades/facultades')
my_spidy.get_units()
my_spidy.get_all_links()



        
