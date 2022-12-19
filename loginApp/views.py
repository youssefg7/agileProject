from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from userApp.views import index
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
    churches = models.Church.objects.all()
    ch = []
    for x in churches:
        ch.append(x)
    return render(request, "donorLoginApp/donorSignup.html", {'Churches': ch})

def donorSignupSubmit(request):
    user1 = models.User(name = request.POST['Name'], email = request.POST['Email'], password = request.POST['Password'], role = 2)
    user1.save()
    l = []
    selected_churches = request.POST.getlist("item_checkbox")
    print(selected_churches)
    for x in selected_churches: print(type(x), x)
    # donor = models.Donor(models.User.objects.get(user_id = user1.user_id), fav_church = l)
    # donor.save()
    return HttpResponseRedirect('/')

def donorLogout(request):
    response = HttpResponseRedirect('/')
    max_age = 365 * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),"%a, %d-%b-%Y %H:%M:%S GMT",)
    response.set_cookie("userid", '0', max_age=max_age,expires=expires,)
    return response