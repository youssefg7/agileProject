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
    clearAlert(request);
    return render(request, "donorLoginApp/donorLogin.html")

def donorLoginSubmit(request):
    femail = request.POST['Email']
    fpassword = request.POST['Password']
    fquery = models.User.objects.filter(email=femail)
    if fquery.all().count() == 0:
        makeAlert(request, 1, "Wrong Email")
        return redirect('donorLoginPage')
    else:
        if fquery.all().values()[0]["password"] == fpassword:
                response = HttpResponseRedirect('/')
                max_age = 365 * 24 * 60 * 60
                expires = datetime.strftime(datetime.utcnow() + timedelta(seconds=max_age),"%a, %d-%b-%Y %H:%M:%S GMT",)
                response.set_cookie("userid", fquery.all().values()[0]["user_id"], max_age=max_age,expires=expires,)
                makeAlert(request, 2, "Logged in")
                return response
        else:
            makeAlert(request, 1, "Wrong Password")
            return redirect('donorLoginPage')

def donorSignupPage(request):
    clearAlert(request)
    churches = getAllChurches()
    return render(request, "donorLoginApp/donorSignup.html", {'Churches': churches})

def donorSignupSubmit(request):
    name = request.POST['Name']
    email = request.POST['Email']
    password = request.POST['Password']
    donor = saveUser(name, email, 'Donor', password)
    if donor == False:
        makeAlert(request, 1, "Email is Registered Before")
        return redirect('donorSignup')
    selected_churches = request.POST.getlist("item_checkbox")
    churches = []
    for i in selected_churches:
        churches.append(getChurch(int(i)))
    donor.fav_church.set(churches)
    print(churches)
    donor.save()
    makeAlert(request, 2, "Signup Done")
    return redirect('donorLoginPage')

def donorLogout(request):
    makeAlert(request, 2, "Logout successfully")
    response = HttpResponseRedirect('/')
    max_age = 365 * 24 * 60 * 60
    expires = datetime.strftime(datetime.utcnow() + timedelta(seconds=max_age),"%a, %d-%b-%Y %H:%M:%S GMT",)
    response.set_cookie("userid", '0', max_age=max_age,expires=expires,)
    return response