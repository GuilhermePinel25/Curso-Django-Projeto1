from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'recipes/home.html')

def contato(request):
    # return HTTP Response
    return HttpResponse('Contato')

def sobre(request):
    # return HTTP Response
    return HttpResponse('Sobre')