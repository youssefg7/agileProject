from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from dbApp import models
from Util import *

def adminInvPage(request):
    try:
        id = getId(request)
        user = getUser(id)
        church = getAdminChurch(id)
        all_items = getItemDetailsFiltered(church)
        l = len(all_items)
        items = zip(list(range(1, l+1)), all_items)
        dict = {'user':user, 'church': church, 'items': items}
    except:
        dict = {'role' : "Anon", 'name': "", 'rolenum': -1}
    return render(request, "userApp/admininv.html",dict)

def adminPeopleINPage(request):
    try:
        id = getId(request)
        user = getUser(id)
        church = getAdminChurch(id)
        all_needs = getNeedsFiltered(church)
        l = len(all_needs)
        needs = zip(list(range(1, l+1)), all_needs)
        today = datetime.today().date
        dict = {'user':user, 'church': church, 'needs': needs, 'today':today }
    except:
        dict = {'role' : "Anon", 'name': "", 'rolenum': -1}
    return render(request, "userApp/adminPeopleIN.html",dict)

def index(request):
    if request.session['done'] == 0:
        request.session['done'] = 1
    else:
        request.session['alert'] = 0
        request.session['message'] = ""
    try:
        id = getId(request)
        user = getUser(id)
        if user.role.role_number == 2:
            churches = getAllChurches()
            cards = getCardsFiltered(id)
            ts = getAllTimeSlots(30)
            dict = {'user':user, 'churches': churches, 'cards': cards, 'timeslots': ts}
        elif user.role.role_number == 1:
            church = getAdminChurch(id)
            all_items = getItemDetailsFiltered(church)
            all_needs = getNeedsFiltered(church)
            items = zip(list(range(1, min(5, len(all_items)) + 1)), all_items)
            needs = zip(list(range(1, min(5, len(all_needs)) + 1)), all_needs)
            today = datetime.today().date
            dict = {'user':user, 'church': church, 'items': items,'needs': needs, 'today': today}
        else:
            raise KeyError()
    except:
        dict = {'role' : "Anon", 'name': "", 'rolenum': -1}
    return render(request, "userApp/index.html", dict) 

def Giveout(request):
    selected_need = request.POST.get('Giveout')
    need = models.Need.objects.get(id = selected_need)
    church = need.church_id
    item = need.item_id
    
    if not saveItemDetailsGiveout(church, item, need):
        request.session['done'] = 0
        request.session['alert'] = 1
        request.session['message'] = "Can't Giveout This Item"
        return redirect('userApp:index')
    needDueDateAlter(need)
    request.session['done'] = 0
    request.session['alert'] = 2
    request.session['message'] = "Giveout Done"
    return redirect('userApp:index')

def onlineDonation(request):
    id = getId(request)
    amount = request.POST['Amount']
    selected_card = request.POST.get('card_dropdown')
    church = int(request.POST.get('church_dropdown'))
    if church == 0:
        request.session['done'] = 0
        request.session['alert'] = 1
        request.session['message'] = "Please Select a Church"
        return redirect('userApp:index')
    if selected_card == '0':
        church = getChurch(church)
        cardNumber = request.POST['Cardnum']
        holderName = request.POST['Cardholdname']
        CVV = int(request.POST['CVV'])
        expiryDate = request.POST['Expiry']   
        expiryDate = datetime.strptime(expiryDate, '%Y-%m').date()
        try:
            save = request.POST['saveCard']
        except:
            save = ''
        if not checkOnlineDonation(cardNumber, CVV, expiryDate):
            request.session['done'] = 0
            request.session['alert'] = 1
            request.session['message'] = "Enter Valid Card Info"
            return redirect('userApp:index')       
        if save == 'on':
            saveCard(id, cardNumber, CVV, expiryDate)
    amount = toInt(amount)
    item = getItemByName('Cash')
    donor = getDonor(id)
    saveReciept(donor, church, item, amount)
    saveItemDetails(church, item, amount)
    request.session['done'] = 0
    request.session['alert'] = 2
    request.session['message'] = "Donation Done"
    return redirect('userApp:index')

def inPersonDonation(request):
    id = request.COOKIES['userid']
    selected_church = int(request.POST.get('church_dropdown2'))
    selected_timeslot = request.POST.get('timeslot_dropdown')
    meeting_date = request.POST['meeting_date']
    ret = saveReservation(id, selected_church, meeting_date, selected_timeslot)
    if ret != 0:
        request.session['done'] = 0
        request.session['alert'] = 1
        if ret == 1:
            request.session['message'] = "Please Select a church"
        if ret == 2:
            request.session['message'] = "Plase Select Appropriate Date"
        if ret == 3:
            request.session['message'] = "Already Reserved"
        return redirect('userApp:index')  
    request.session['done'] = 0
    request.session['alert'] = 2
    request.session['message'] = "Reservation Done"
    return redirect('userApp:index')

def aboutPage(request):
    try:
        id = getId(request)
        user = (id)
        state = 1
        dict = {'user':user, 'state': state}
    except:
        state = 2
        dict = {'role' : "", 'name': "", 'state': state, 'rolenum': -1}
    return render(request, "userApp/about.html", dict)