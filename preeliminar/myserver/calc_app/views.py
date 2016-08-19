from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def sumar(request):
    return render(request, 'sumar.html')

def restar(request):
    return render(request, 'restar.html')

def potencias(request):
    return render(request, 'potencias.html')

