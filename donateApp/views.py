from django.shortcuts import render
from django.http import HttpResponse
from dbApp import models

# Create your views here.

def index(request):
    try:
        x = models.User.objects.get(user_id = request.COOKIES['userid']).name
    except:
        x = "Please Login"
    return render(request, "donateApp/index.html", {'test' : x}) 
