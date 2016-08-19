from django.conf.urls import url
from . import views

urlpatterns = [
    #localhost/sumar
    url(r'^sumar/', views.sumar),
    #localhost/restar
    url(r'^restar/', views.restar),
    #localhost/potencias
    url(r'^potencias/', views.potencias),
    #localhost. Va de ultimas porque no se Regex
    url(r'^', views.home),
]
