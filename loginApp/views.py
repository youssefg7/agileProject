from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    
    x = "login"
    return render(request, "loginApp/index.html", {'test' : x}) 

# Create your views here.
