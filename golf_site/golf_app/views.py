# from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):

    # return HttpResponse("<h1> Text Homepage <h1>")
    return render(request, 'base.html')