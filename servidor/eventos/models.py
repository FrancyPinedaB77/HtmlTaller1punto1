import json
from os import listdir
from os.path import realpath
from django.db import models
from os.path import realpath

# Create your models here.

def get_units(path):
    files = listdir(path)
    dicts = []
    for filename in files:
        with open(path+'/'+filename) as json_data:
            dicts.append(json.load(json_data))
    return dicts

def filter_before(date, units):
    events = []
    for unit in units:
        events_site = unit['events_site']
        if events_site:
            events += filter(lambda x: x['date'] < date, events_site['events'])
    return events

def filter_after(date, units):
    events = []
    for unit in units:
        events_site = unit['events_site']
        if events_site:
            events += filter(lambda x: x['date'] > date, events_site['events'])
    return events

PATH = realpath('./bin/punto1')
units = get_units(PATH+'/jsons')
print(filter_before("2016-08-10T00:00:00", units))
