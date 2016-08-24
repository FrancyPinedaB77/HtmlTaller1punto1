import re
from urllib import request


def fixRelative(relative, head):
   if 'http' in relative:
      return relative
   return head + relative

def getUnits(root):
   units = re.findall('<li><a\s+href="https?://([^"]+uniandes\.edu\.co)[^"]*"\s+[^>]*>([^<]*(Facultad|Centro|Escuela|Departamento)[^<]*)</a></li>', root)
   units = list(set([i[:2] for i in units]))
   units.sort(key=lambda i: i[1])
   return units

def getCalendar(links):
   match = re.findall('(http://.+/)(day|month|year)\.(listevents|calendar)', links)
   if len(match) > 0:
      return match[0][0]+'year.'+match[0][2]+'/'
   return None
   
with request.urlopen('http://uniandes.edu.co/institucional/facultades/facultades') as response:
   root = response.read().decode()

units = getUnits(root)
   
for (url, name) in units:
    url = 'http://{}'.format(url)
    print('Searching events site for', name, 'at', url)
    unit_site = None
    try:
        with request.urlopen(url) as response:
            unit_site = response.read().decode()
    except:
        print('Request failed!!!')

    if unit_site:
        events_links = re.findall('href=["\']([^\'"]*([Ee]ventos|icagenda|icalrepeat|listevents)[^\'"]*)["\']', unit_site)
        if len(events_links) == 0:
            print(' ','Didn\'t found any link to an events page!')
        else:
            print(' ','Links to events found:')
            events_links.sort(key=lambda i: len(i[0]))
            events_links = '\n'.join([fixRelative(i[0],url) for i in events_links])
   
            if getCalendar(events_links):
               print('    Calendar:', getCalendar(events_links))
            else:
               print('   ',events_links)
   
    print('')
