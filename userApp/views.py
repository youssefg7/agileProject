from datetime import date, datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from dbApp import models

# Create your views here.

def adminInvPage(request):
    try:
        id = request.COOKIES['userid']
        user = models.User.objects.get(user_id = id)
        array = [1,2]
        
        church = models.Admin.objects.get(user_id = id)
        church = church.church_id
        all_items = models.ItemDetails.objects.filter(church_id = church)
        list1 = []
        list2 = []
        i = 0
        for x in all_items:
            list1.append(x.item_id)
            list2.append(x.quantity)
            i += 1
        items = zip(list(range(1, i+1)), list1, list2)
        dict = {'user':user, 'church': church, 'items': items, 'array': array}
    except:
        dict = {'role' : "Anon", 'name': "", 'rolenum': -1}
    return render(request, "userApp/admininv.html",dict)

def adminPeopleINPage(request):
    try:
        id = request.COOKIES['userid']
        user = models.User.objects.get(user_id = id)
        array = [1,2]
        
        church = models.Admin.objects.get(user_id = id)
        church = church.church_id
        all_needs = models.Need.objects.filter(church_id = church)

        i = len(all_needs)
        needs = zip(list(range(1, i+1)), all_needs)
        today = datetime.today().date
        dict = {'user':user, 'church': church, 'needs': needs, 'array': array, 'today':today }
    except:
        dict = {'role' : "Anon", 'name': "", 'rolenum': -1}
    return render(request, "userApp/adminPeopleIN.html",dict)


def datetime_range(start, end, delta):
        current = start
        while current < end:
            yield current
            current += delta

def index(request):
    try:
        id = request.COOKIES['userid']
        user = models.User.objects.get(user_id = id)
        array = [1,2]
        if user.role.role_number == 2:
            churches = models.Church.objects.all()
            cards = models.Card.objects.filter(user_id = id)

            ts = [dt.strftime('%H:%M') for dt in 
                datetime_range(datetime(2016, 9, 1, 10), datetime(2016, 9, 1, 8+12, 30), 
                timedelta(minutes=30))]

            dict = {'user':user, 'array': array, 'churches': churches, 'cards': cards, 'timeslots': ts}
        elif user.role.role_number == 1:
            church = models.Admin.objects.get(user_id = id)
            church = church.church_id

            all_items = models.ItemDetails.objects.filter(church_id = church)
            all_needs = models.Need.objects.filter(church_id = church)

            items = zip(list(range(1, min(5, len(all_items)) + 1)), all_items)
            needs = zip(list(range(1, min(5, len(all_needs)) + 1)), all_needs)
            today = datetime.today().date

            dict = {'user':user, 'church': church, 'items': items, 'array': array, 'needs': needs, 'today': today}
        else:
            raise KeyError()
    except:
        dict = {'role' : "Anon", 'name': "", 'rolenum': -1}

    return render(request, "userApp/index.html", dict) 

def Giveout(request):
    selected_need = request.POST.get('Giveout')
    need = models.Need.objects.get(id = selected_need)
    print(need.church_id.name)
    print(need.item_id.name)
    try:
        item = models.ItemDetails.objects.get(church_id = need.church_id, item_id = need.item_id)
    except:
        return HttpResponseRedirect('/')
        # alert
    if item.quantity > need.quantity:
        item.quantity -= need.quantity
        item.save()
    else:
        return HttpResponseRedirect('/about')
        # alert
    if need.period == 0:
        need.delete()
    else:
        need.due_date += timedelta(days=need.period)
        need.save()
    return HttpResponseRedirect('/')

def onlineDonation(request):
    id = request.COOKIES['userid']
    amount = request.POST['Amount']
    selected_card = request.POST.get('card_dropdown')
    church = int(request.POST.get('church_dropdown'))
    if selected_card == '0':
        if church == 0:
            return HttpResponseRedirect('/', {'alert': 1})
            # alert

        church = models.Church.objects.get(church_id = church)
        print(church)
        cardNumber = request.POST['Cardnum']
        holderName = request.POST['Cardholdname']
        CVV = int(request.POST['CVV'])
        
        try:
            save = request.POST['saveCard']
        except:
            save = ''
        
        expiryDate = request.POST['Expiry']   
        if cardNumber > '9999999999999999' or cardNumber < '1000000000000000':
            return HttpResponseRedirect(reverse('index'))
            # alert
        if CVV > 999 or CVV < 111:
            return HttpResponseRedirect(reverse('index'))
            # alert
        
        expiryDate = datetime.strptime(expiryDate, '%Y-%m').date()
        if date.today().year > expiryDate.year:
            return HttpResponseRedirect(reverse('index'))
            # alert
        if date.today().month > expiryDate.month and date.today().year == expiryDate.year:
            return HttpResponseRedirect(reverse('index'))
            # alert
        print(save)
        if save == 'on':
            card = models.Card(user_id = models.Donor.objects.get(user_id = id), card_num = cardNumber, cvv = CVV, expiry_date = expiryDate)
            card.save()

    if amount != '':
        amount = int(amount)

    reciept = models.Reciept(
                date = datetime.now().date(),
                time = datetime.now().time(), 
                user_id = models.Donor.objects.get(user_id = id), 
                church_id = models.Church.objects.get(church_id = church))

    reciept.save()
    r_details = models.R_Details(
                reciept_id = reciept, item_id = models.Item.objects.get(name = 'Cash'), 
                item_quantity = amount)
    r_details.save()

    cash_id = models.Item.objects.get(name = 'Cash')
    
    try:
        cash_item = models.ItemDetails.objects.get(church_id = church, item_id = cash_id)
        cash_item.quantity += amount
        cash_item.save()

    except:
        item_cash = models.ItemDetails(
                    church_id = models.Church.objects.get(church_id = church), # check church_id = church
                    item_id = models.Item.objects.get(name = 'Cash'),
                    quantity = amount
        )
        item_cash.save()

    return HttpResponseRedirect('/')

def inPersonDonation(request):

    id = request.COOKIES['userid']
    selected_church = int(request.POST.get('church_dropdown2'))
    selected_timeslot = request.POST.get('timeslot_dropdown')
    meeting_date = request.POST['meeting_date']

    try:
        reserved = models.Reserves.objects.filter(church_id = selected_church, date = meeting_date, time = selected_timeslot)
        print(reserved)
        if len(reserved) > 0:
            raise KeyError()
        reserves = models.Reserves(
                    user_id = models.Donor.objects.get(user_id = id),
                    church_id = models.Church.objects.get(church_id = selected_church),
                    date = meeting_date, 
                    time = selected_timeslot
        )

        reserves.save()

    except:
        return HttpResponseRedirect('/about')
        # alert

    return HttpResponseRedirect('/')


def aboutPage(request):
    try:
        id = request.COOKIES['userid']
        user = models.User.objects.get(user_id = id)
        state = 1
        dict = {'user':user, 'state': state}
    except:
        state = 2
        dict = {'role' : "", 'name': "", 'state': state, 'rolenum': -1}
    
    return render(request, "userApp/about.html", dict)