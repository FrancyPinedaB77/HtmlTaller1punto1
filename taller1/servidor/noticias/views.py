from django.shortcuts import render
from . import models
from .forms import SearchForm

# Create your views here.
def index(request):
    newsReader = models.NewsReader('data_full.xml')
    filterlist = []
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            filterlist = newsReader.filter(form.cleaned_data['search'],form.cleaned_data['kind'])
    else:
        form = SearchForm()
    context = {'newslist': newsReader.news, 'filterlist': filterlist , 'form': form}
    return render(request, 'noticias.html', context)
