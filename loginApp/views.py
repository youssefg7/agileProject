from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from donateApp.views import index
from dbApp import models
import datetime

def donorLoginPage(request):
    return render(request, "donorLoginApp/donorLogin.html")

def donorLoginSubmit(request):
    femail = request.POST['Email']
    fpassword = request.POST['Password']
    fquery = models.User.objects.filter(email=femail)
    if fquery.all().count() == 0:
        return HttpResponseRedirect(reverse('donorLoginPage'))
    else:
        if fquery.all().values()[0]["password"] == fpassword:
                response = HttpResponseRedirect('/')
                max_age = 365 * 24 * 60 * 60
                expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),"%a, %d-%b-%Y %H:%M:%S GMT",)
                response.set_cookie("userid", fquery.all().values()[0]["user_id"], max_age=max_age,expires=expires,)
                return response
        else:
            return HttpResponseRedirect(reverse('donorLoginPage'))
        
def myaccountPage(request):
    return render(request, "donorLoginApp/donorMyaccount.html")

def donorSignupPage(request):
    return render(request, "donorLoginApp/donorSignup.html")

def donorLogout(request):
    response = HttpResponseRedirect('/')
    max_age = 365 * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),"%a, %d-%b-%Y %H:%M:%S GMT",)
    response.set_cookie("userid", '0', max_age=max_age,expires=expires,)
    return response