from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    x = "test"
    return render(request, "donateApp/index.html", {'test' : x}) 
