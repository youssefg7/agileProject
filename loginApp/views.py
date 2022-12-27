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
    if user.role.role_number == 1:
        church = models.Admin.objects.get(user_id = id).church_id
        churches = models.Church.objects.filter(~Q(church_id = church.church_id))
        items = models.Item.objects.all()
        people = models.PeopleInNeed.objects.all()
        donors = models.Donor.objects.all()
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
    id = request.COOKIES['userid']
    email = request.POST['Email']
    mails = models.User.objects.filter(email = email)
    if len(mails) > 0:
        return HttpResponseRedirect('/about')
        # alert
    name = request.POST['Name']
    user = models.User(email = email, name = name, password = 'Admin', role = models.Roles.objects.get(role_name = 'Admin'))
    user.save()
    church = models.Admin.objects.get(user_id = id).church_id
    admin = models.Admin(user_id = user, church_id = church)
    admin.save()
    return HttpResponseRedirect('/')

def addpeopleinneedSubmit(request):
    id = request.COOKIES['userid']
    person = request.POST.get('people_dropdown')
    item = request.POST['item_datalist1']
    quantity = request.POST['Quantity1']
    period = request.POST['Period']
    date = request.POST['due_date']

    church = models.Admin.objects.get(user_id = id).church_id
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    
    if quantity != '':
        quantity = int(quantity)
    
    if period != '':
        period = int(period)

    try:
        item = models.Item.objects.get(name = item)
    except:
        item = models.Item(name = item)
        item.save()
        
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
        person = models.PeopleInNeed.objects.get(id = person)

    try:
        need = models.Need.objects.filter(church_id = church).get(item_id = item.item_id, people_in_need_id = person.id)
        need.quantity += quantity
        need.save()
    except:
        if quantity == '' or period == '':
            pass
            # alert
        need = models.Need(church_id = church, item_id = item, people_in_need_id = person, quantity = quantity, due_date = date, period = period)
        need.save()


    return HttpResponseRedirect('/')

def inventorySubmit(request):
    id = request.COOKIES['userid']
    donor = request.POST.get('donor_dropdown')
    item = request.POST['item_datalist2']
    quantity = request.POST['Quantity2']

    church = models.Admin.objects.get(user_id = id).church_id
    date = datetime.datetime.today()
    
    if quantity != '':
        quantity = int(quantity)
    else:
        pass
        # alert

    try:
        item = models.Item.objects.get(name = item)
    except:
        item = models.Item(name = item)
        item.save()
        
    if donor == '-1':
        name = request.POST['donor_name']
        email = request.POST['donor_email']
        if name == '' or email == '':
            pass
            # alert
        user = models.User(name = name, email = email, role = models.Roles.objects.get(role_name = 'Donor'), password = 'Donor')
        user.save()
        donor = models.Donor(user_id = user)
        donor.save()
    elif donor == '0':
        pass
        # alert
    else:
        donor = models.Donor.objects.get(user_id = int(donor))


    reciept = models.Reciept(
                date = datetime.datetime.now().date(),
                time = datetime.datetime.now().time(), 
                user_id = donor, 
                church_id = church)
    reciept.save()

    r_details = models.R_Details(
                reciept_id = reciept, item_id = item, 
                item_quantity = quantity)
    r_details.save()

    
    try:
        item_details = models.ItemDetails.objects.get(church_id = church, item_id = item)
        item_details.quantity += quantity

    except:
        item_details = models.ItemDetails(
                    church_id = church,
                    item_id = item,
                    quantity = quantity)
    
    item_details.save()

    return HttpResponseRedirect('')

def donorSignupPage(request):
    churches = models.Church.objects.all()
    return render(request, "donorLoginApp/donorSignup.html", {'Churches': churches})

def donorSignupSubmit(request):
    user1 = models.User(name = request.POST['Name'], email = request.POST['Email'], password = request.POST['Password'], role = models.Roles.objects.get(role_name = 'Donor'))
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