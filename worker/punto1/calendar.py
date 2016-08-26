import requests
from lxml import html

def foo(url):
    print(url)
    page = requests.get(url)

    tree = html.fromstring(page.content)
    x = tree.xpath('//td[@class="cal_td_daysnames"]/../..//ul//a[@class="ev_link_row"]')
    for i in x:
        print(i.text_content(), i.get('href'))
    print('')
    
foo('http://fisica.uniandes.edu.co/index.php/es/agenda/year.listevents/')
foo('https://economia.uniandes.edu.co/facultad/eventos-economia/year.listevents/')
foo('https://administracion.uniandes.edu.co/index.php/es/facultad/sobre-la-facultad/eventos/year.listevents/')
