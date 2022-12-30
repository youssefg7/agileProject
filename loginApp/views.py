from urllib import response
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from userApp.views import index
from dbApp import models
from datetime import datetime, timedelta
from django.db.models import Q
from Util import *

def donorLoginPage(request):
    if request.session['done'] == 0:
        request.session['done'] = 1
    else:
        request.session['alert'] = 0
        request.session['message'] = ""
    return render(request, "donorLoginApp/donorLogin.html")

def donorLoginSubmit(request):
    femail = request.POST['Email']
    fpassword = request.POST['Password']
    fquery = models.User.objects.filter(email=femail)
    if fquery.all().count() == 0:
        request.session['done'] = 0
        request.session['alert'] = 1
        request.session['message'] = "Wrong Email"
        return redirect('donorLoginPage')
    else:
        if fquery.all().values()[0]["password"] == fpassword:
                response = HttpResponseRedirect('/')
                max_age = 365 * 24 * 60 * 60
                expires = datetime.strftime(datetime.utcnow() + timedelta(seconds=max_age),"%a, %d-%b-%Y %H:%M:%S GMT",)
                response.set_cookie("userid", fquery.all().values()[0]["user_id"], max_age=max_age,expires=expires,)
                request.session['done'] = 0
                request.session['alert'] = 2
                request.session['message'] = "Logged in"
                return response
        else:
            request.session['done'] = 0
            request.session['alert'] = 1
            request.session['message'] = "Wrong Password"
            return redirect('donorLoginPage')

def donorSignupPage(request):
    if request.session['done'] == 0:
        request.session['done'] = 1
    else:
        request.session['alert'] = 0
        request.session['message'] = ""
    churches = getAllChurches()
    return render(request, "donorLoginApp/donorSignup.html", {'Churches': churches})

def donorSignupSubmit(request):
    name = request.POST['Name']
    email = request.POST['Email']
    password = request.POST['Password']
    donor = saveUser(name, email, 'Donor', password)
    if donor == False:
        request.session['done'] = 0
        request.session['alert'] = 1
        request.session['message'] = "Email is Registered Before"
        return redirect('donorSignup')
    selected_churches = request.POST.getlist("item_checkbox")
    churches = []
    for i in selected_churches:
        churches.append(getChurch(int(i)))
    donor.fav_church.set(churches)
    print(churches)
    donor.save()
    request.session['done'] = 0
    request.session['alert'] = 2
    request.session['message'] = "Signup Done"
    return redirect('donorLoginPage')

def donorLogout(request):
    response = HttpResponseRedirect('/')
    max_age = 365 * 24 * 60 * 60
    expires = datetime.strftime(datetime.utcnow() + timedelta(seconds=max_age),"%a, %d-%b-%Y %H:%M:%S GMT",)
    response.set_cookie("userid", '0', max_age=max_age,expires=expires,)
    return response