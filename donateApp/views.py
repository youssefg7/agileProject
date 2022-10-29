from django.shortcuts import render
from django.http import HttpResponse
from .models import Members

# Create your views here.

def index(request):
    mymembers = Members.objects.all().values()
    x = mymembers[0]["firstname"]
    return render(request, "donateApp/index.html", {'test' : x}) 
