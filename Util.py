from datetime import date, datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from dbApp import models
from django.db.models import Q

def datetime_range(start, end, delta):
        current = start
        while current < end:
            yield current
            current += delta

def getId(request):
    return request.COOKIES['userid']

def getUser(id):
    return models.User.objects.get(user_id = id)

def getAdminChurch(admin_id):
    return models.Admin.objects.get(user_id = admin_id).church_id

def getAllChurchesExcept(church):
    return models.Church.objects.filter(~Q(church_id = church))

def getAllItems():
    return models.Item.objects.all()

def getAllPeopleInNeed():
    return models.PeopleInNeed.objects.all()

def getAllDonors():
    return models.Donor.objects.all()

def getAllChurches():
    return models.Church.objects.all()

def getItemDetailsFiltered(church):
    return models.ItemDetails.objects.filter(church_id = church)

def getItemDetails(church, item):
    return models.ItemDetails.objects.get(church_id = church, item_id = item)

def getNeedsFiltered(church):
    return models.Need.objects.filter(church_id = church)

def getCardsFiltered(id):
    return models.Card.objects.filter(user_id = id)

def getPeopleInNeed(id):
    models.PeopleInNeed.objects.get(id = id)

def getAllTimeSlots(minute_difference):
    return [dt.strftime('%H:%M') for dt in 
                datetime_range(datetime(2016, 9, 1, 10), datetime(2016, 9, 1, 8+12, 30), 
                timedelta(minutes=minute_difference))]

def needDueDateAlter(need):
    if need.period == 0:
        need.delete()
    else:
        need.due_date += timedelta(days=need.period)
        need.save()

def getChurch(church):
    return models.Church.objects.get(church_id = church)

def getDonor(id):
    return models.Donor.objects.get(user_id = id)

def getItemByName(name):
    try:
        item = models.Item.objects.get(name = name)
    except:
        item = models.Item(name = name)
        item.save()
    return item

def toInt(x):
    if x != '':
        x = int(x)
    else:
        x = 0

def checkOnlineDonation(cardNumber, CVV, date):
    if cardNumber > '9999999999999999' or cardNumber < '1000000000000000':
            return False
    if CVV > 999 or CVV < 111:
        return False
    if date.today().year > date.year:
            return HttpResponseRedirect(reverse('index'))
    if date.today().month > date.month and date.today().year == date.year:
        return HttpResponseRedirect(reverse('index'))
    return True

def saveCard(id, cardNumber, CVV, expiryDate):
    card = models.Card(user_id = getDonor(id), 
                               card_num = cardNumber, 
                               cvv = CVV, 
                               expiry_date = expiryDate)
    card.save()

def saveReciept(donor, church, item, quantity):
    reciept = models.Reciept(
                date = datetime.now().date(),
                time = datetime.now().time(), 
                user_id = donor, 
                church_id = church)
    reciept.save()

    r_details = models.RecieptDetails(
                reciept_id = reciept, item_id = item, 
                item_quantity = quantity)
    r_details.save()


def saveItemDetails(church, item, quantity):
    try:
        item_details = getItemDetails(church, item)
        item_details.quantity += quantity
    except:
        item_details = models.ItemDetails(
                    church_id = church,
                    item_id = item,
                    quantity = quantity
        )
    item_details.save()

def saveItemDetailsGiveout(church, item, need):
    try:
        item_details = getItemDetails(church, item)
    except:
        return False
    if item_details.quantity > need.quantity:
        item_details.quantity -= need.quantity
        item_details.save()
    else:
        return False
    return True

def saveReservation(id, church, date, timeslot):
    reserved = models.Reservation.objects.filter(church_id = church, date = date, time = timeslot)
    if len(reserved) > 0:
        return False
    reserves = models.Reservation(
                user_id = getDonor(id),
                church_id = getChurch(church),
                date = date, 
                time = timeslot
    )
    reserves.save()

    return True

def getRole(name):
    try:
        role = models.Roles.objects.get(role_name = name)
    except:
        role = models.Item(role_name = name)
        role.save()
    return role

def saveUser(name, email, role_name, password, church):
    role = getRole(role_name)
    user = models.User(name = name, email = email, role = role, password = password)
    user.save()
    if role_name == 'Donor':
        donor = models.Donor(user_id = user)
        donor.save()
        return donor
    elif role_name == 'Admin':
        admin = models.Admin(user_id = user, chuch_id = church)
        admin.save()
        return admin

def changeSaveNeed(church, item, person, quantity, date, period):
    try:
        need = models.Need.objects.filter(church_id = church).get(item_id = item.item_id, people_in_need_id = person.id)
        need.quantity += quantity
    except:
        need = models.Need(church_id = church, item_id = item, people_in_need_id = person, quantity = quantity, due_date = date, period = period)
    need.save()
    
def getAllEmailsFiltered(email):
    return models.User.objects.filter(email = email)