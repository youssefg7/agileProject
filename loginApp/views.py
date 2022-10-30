from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from donateApp.views import index
from dbApp import models
import datetime

def loginPage(request):
    return render(request, "loginApp/login.html")

def loginSubmit(request):
    femail = request.POST['Email']
    fpassword = request.POST['Password']
    fquery = models.User.objects.filter(email=femail)
    if fquery.all().count() == 0:
        return HttpResponseRedirect(reverse('loginPage'))
    else:
        if fquery.all().values()[0]["password"] == fpassword:
                response = HttpResponseRedirect(reverse('index'))
                max_age = 365 * 24 * 60 * 60
                expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),"%a, %d-%b-%Y %H:%M:%S GMT",)
                response.set_cookie("userid", fquery.all().values()[0]["user_id"], max_age=max_age,expires=expires,)
                return response
        else:
            return HttpResponseRedirect(reverse('loginPage'))
        



# Create your views here.
