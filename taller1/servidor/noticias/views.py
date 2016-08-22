from django.shortcuts import render
from . import models
from .forms import SearchForm

# Create your views here.
def index(request):
    newsReader = models.NewsReader('data_full.xml')
    regexlist = [] # Lista de noticias filtradas con regex
    xquerylist = [] # Lista de noticias filtradas con xquery
    if request.method == 'POST': 
        form = SearchForm(request.POST)
        if form.is_valid():
            regexlist = newsReader.filter(form.cleaned_data['search'],form.cleaned_data['kind'])
            xquerylist = regexlist
    else:
        form = SearchForm()
    context = {'newslist': newsReader.news, 'regexlist': regexlist, 'xquerylist': xquerylist , 'form': form}
    return render(request, 'noticias.html', context)
