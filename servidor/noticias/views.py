from django.shortcuts import render
from . import models
from .forms import SearchForm

# Create your views here.

newsReader = models.NewsReader()
def index(request):
    newsReader.get_news()
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
