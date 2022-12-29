from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from userApp.views import index
from dbApp import models
import datetime
from django.db.models import Q
from Util import *

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
    id = getId(request)
    user = getUser(id)
    if user.role.role_number == 1:
        church = getAdminChurch(id)
        churches = getAllChurchesExcept(church.church_id)
        items = getAllItems()
        people = getAllPeopleInNeed()
        donors = getAllDonors()
        dict = {'user':user, 'church': church, 'churches':churches, 'items':items, 'people':people, 'donors': donors}
    elif user.role.role_number == 2:
        dict = {'user':user}
    return render(request, "donorLoginApp/donorMyaccount.html", dict)

def myAccountSubmit(request):
    id = request.COOKIES['userid']
    user = models.User.objects.get(user_id = id)
    name = request.POST['Name']
    password = request.POST['Password']
    print(user.password)
    if name != '':
        user.name = name
    if password != '':
        user.password = password
    print(user.password)
    user.save()
    if user.role.role_number == 1:
        admin = models.Admin.objects.get(user_id = user.user_id)
        church = request.POST.get('church_dropdown')
        if church != '0':
            admin.church_id = models.Church.objects.get(church_id = church)
        admin.save()
    return HttpResponseRedirect('/')

def addAdminSubmit(request):
    id = getId(request)
    email = request.POST['Email']
    mails = getAllEmailsFiltered(email)
    if len(mails) > 0:
        return HttpResponseRedirect('/')
        # alert
    name = request.POST['Name']
    church = getAdminChurch(id)
    saveUser(name, email, 'Admin', 'Admin', church)
    return HttpResponseRedirect('/')

def addpeopleinneedSubmit(request):
    id = request.COOKIES['userid']
    person = request.POST.get('people_dropdown')
    item = request.POST['item_datalist1']
    quantity = request.POST['Quantity1']
    period = request.POST['Period']
    date = request.POST['due_date']
    church = getAdminChurch(id)
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    quantity = toInt(quantity)
    period = toInt(period)
    item = getItemByName(item)
    if person == '-1':
        name = request.POST['person_name']
        ID = request.POST['person_ID']
        if name == '' or ID == '':
            pass
            # alert
        person = models.PeopleInNeed(id = ID, name = name)
        person.save()
    elif person == '0':
        pass
        # alert
    else:
        person = getPeopleInNeed(person)
    changeSaveNeed(church, item, person, quantity, date, period)
    return HttpResponseRedirect('/')

def inventorySubmit(request):
    id = getId(request)
    donor = request.POST.get('donor_dropdown')
    item = request.POST['item_datalist2']
    quantity = request.POST['Quantity2']
    church = getAdminChurch(id)
    quantity = toInt(quantity)
    item = getItemByName(item)
    if donor == '-1':
        name = request.POST['donor_name']
        email = request.POST['donor_email']
        if name == '' or email == '':
            pass
            # alert
        donor = saveUser(name, email, 'Donor', 'Donor')
    elif donor == '0':
        pass
        # alert
    else:
        donor = getDonor(donor)
    saveReciept(donor, church, item, quantity)
    saveItemDetails(church, item, quantity)
    return HttpResponseRedirect('')

def donorSignupPage(request):
    churches = getAllChurches()
    return render(request, "donorLoginApp/donorSignup.html", {'Churches': churches})

def donorSignupSubmit(request):
    name = request.POST['Name']
    email = request.POST['Email']
    password = request.POST['Password']
    donor = saveUser(name, email, 'Donor', password)
    selected_churches = request.POST.getlist("item_checkbox")
    churches = []
    for i in selected_churches:
        churches.append(getChurch(int(i)))
    donor.fav_church.set(churches)
    print(churches)
    donor.save()
    return HttpResponseRedirect('/')

def donorLogout(request):
    response = HttpResponseRedirect('/')
    max_age = 365 * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),"%a, %d-%b-%Y %H:%M:%S GMT",)
    response.set_cookie("userid", '0', max_age=max_age,expires=expires,)
    return response