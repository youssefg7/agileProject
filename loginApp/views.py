from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from userApp.views import index
from dbApp import models
import datetime
from django.db.models import Q

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
    id = request.COOKIES['userid']
    user = models.User.objects.get(user_id = id)
    if user.role == 1:
        church = models.Admin.objects.get(user_id = id).church_id
        churches = models.Church.objects.filter(~Q(church_id = church.church_id))
        items = models.Item.objects.all()
        people = models.PeopleInNeed.objects.all()
        dict = {'user':user, 'church': church, 'churches':churches, 'items':items, 'people':people}
    elif user.role == 2:
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
    if user.role == 1:
        admin = models.Admin.objects.get(user_id = user.user_id)
        church = request.POST.get('church_dropdown')
        if church != '0':
            admin.church_id = models.Church.objects.get(church_id = church)
        admin.save()
    return HttpResponseRedirect('/')

def addAdminSubmit(request):
    id = request.COOKIES['userid']
    email = request.POST['Email']
    mails = models.User.objects.filter(email = email)
    if len(mails) > 0:
        return HttpResponseRedirect('/about')
        # alert
    name = request.POST['Name']
    user = models.User(email = email, name = name, password = 'Admin', role = 1)
    user.save()
    church = models.Admin.objects.get(user_id = id).church_id
    admin = models.Admin(user_id = user, church_id = church)
    admin.save()
    return HttpResponseRedirect('/')

def addpeopleinneedSubmit(request):
    id = request.COOKIES['userid']
    name = request.POST['Peopleinneed']
    item = int(request.POST.get('item_dropdown'))
    quantity = request.POST['Quantity']
    period = request.POST['Period']
    date = request.POST['due_date']
    church = models.Admin.objects.get(user_id = id).church_id
        
    try:
        person = models.PeopleInNeed.objects.get(name = name)
    except:
        person = models.PeopleInNeed(name = name)
        person.save()

    print(item)
    item = models.Item.objects.get(item_id = item)
    
    
    try:
        need = models.Need.objects.filter(church_id = church).get(item_id = item.item_id, people_in_need_id = person.id)
        need.quantity += int(quantity)
        need.save()
    except:
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        need = models.Need(church_id = church, item_id = item, people_in_need_id = person, quantity = int(quantity), due_date = date, period = int(period))
        need.save()
        print(55)


    return HttpResponseRedirect('/')

def donorSignupPage(request):
    churches = models.Church.objects.all()
    return render(request, "donorLoginApp/donorSignup.html", {'Churches': churches})

def donorSignupSubmit(request):
    user1 = models.User(name = request.POST['Name'], email = request.POST['Email'], password = request.POST['Password'], role = 2)
    user1.save()
    selected_churches = request.POST.getlist("item_checkbox")
    churches = []
    donor = models.Donor(user_id = models.User.objects.get(user_id = user1.user_id))
    donor.save()
    for i in selected_churches:
        churches.append(models.Church.objects.get(church_id = int(i)))
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