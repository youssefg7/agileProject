from django.shortcuts import render
from dbApp import models

# Create your views here.

def index(request):
    try:
        y = models.User.objects.get(user_id = request.COOKIES['userid']).role
        role = models.Roles.objects.get(role_number = y).role_name
        name = models.User.objects.get(user_id = request.COOKIES['userid']).name
        state = 1
        dict = {'role' : role, 'name': name, 'state': state, 'rolenum': y}
    except:
        state = 2
        dict = {'role' : "", 'name': "", 'state': state, 'rolenum': -1}
    
    return render(request, "donateApp/index.html", dict) 



def aboutPage(request):
    try:
        y = models.User.objects.get(user_id = request.COOKIES['userid']).role
        role = models.Roles.objects.get(role_number = y).role_name
        name = models.User.objects.get(user_id = request.COOKIES['userid']).name
        state = 1
        dict = {'role' : role, 'name': name, 'state': state, 'rolenum': y}
    except:
        state = 2
        dict = {'role' : "", 'name': "", 'state': state, 'rolenum': -1}
    
    return render(request, "donateApp/about.html", dict)