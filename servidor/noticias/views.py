from django.shortcuts import render
from . import models
from .forms import SearchForm
from time import time
# Create your views here.

newsReader = models.NewsReader()
last  = int(time())

def index(request):
    global last
    now = int(time())
    if (now - last) > 60:
        print(now - last, "seconds since last update... Updating")
        newsReader.get_news()
    else:
       print(now - last, "seconds since last update... Not updating")
    regexlist = [] # Lista de noticias filtradas con regex
    xquerylist = [] # Lista de noticias filtradas con xquery
    if request.method == 'POST': 
        form = SearchForm(request.POST)
        if form.is_valid():
            xquerylist = newsReader.filter_xquery(form.cleaned_data['search'], form.cleaned_data['kind'])
    else:
        form = SearchForm()
    context = {'newslist': newsReader.news, 'regexlist': regexlist, 'xquerylist': xquerylist , 'form': form}
    return render(request, 'noticias.html', context)
