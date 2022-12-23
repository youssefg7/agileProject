from datetime import date, datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from dbApp import models

# Create your views here.

def adminInvPage(request):
    try:
        id = request.COOKIES['userid']
        rolenum = models.User.objects.get(user_id = id).role
        role = models.Roles.objects.get(role_number = rolenum).role_name
        name = models.User.objects.get(user_id = id).name
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
        dict = {'role' : role, 'name': name, 'rolenum': rolenum, 'church': church, 'items': items, 'array': array}
    except:
        dict = {'role' : "Anon", 'name': "", 'rolenum': -1}
    return render(request, "userApp/admininv.html",dict)

def adminPeopleINPage(request):
    try:
        id = request.COOKIES['userid']
        rolenum = models.User.objects.get(user_id = id).role
        role = models.Roles.objects.get(role_number = rolenum).role_name
        name = models.User.objects.get(user_id = id).name
        array = [1,2]
        
        church = models.Admin.objects.get(user_id = id)
        church = church.church_id
        all_needs = models.Need.objects.filter(chuch_id = church)

        list1 = []
        list2 = []
        list3 = []
        list4 = []
        i = 0
        for x in all_needs:   
            list1.append(x.people_in_need_id)
            list2.append(x.item_id)
            list3.append(x.quntity)
            list4.append(x.due_date)
            i += 1

        print(i)
        items = zip(list(range(1, i+1)), list1, list2, list3, list4)
        dict = {'role' : role, 'name': name, 'rolenum': rolenum, 'church': church, 'items': items, 'array': array}
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
        rolenum = models.User.objects.get(user_id = id).role
        role = models.Roles.objects.get(role_number = rolenum).role_name
        name = models.User.objects.get(user_id = id).name
        array = [1,2]
        if rolenum == 2:
            churches = models.Church.objects.all()
            cards = models.Card.objects.filter(user_id = id)

            ts = [dt.strftime('%H:%M') for dt in 
                datetime_range(datetime(2016, 9, 1, 10), datetime(2016, 9, 1, 8+12, 30), 
                timedelta(minutes=30))]

            dict = {'role' : role, 'name': name, 'rolenum': rolenum, 'array': array, 'churches': churches, 'cards': cards, 'timeslots': ts}
        elif rolenum == 1:
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
                if i == 5:
                    break
            items = zip(list(range(1, i+1)), list1, list2)

            all_needs = models.Need.objects.filter(chuch_id = church)

            list3 = []
            list4 = []
            list5 = []
            list6 = []
            j = 0
            for x in all_needs:
                list3.append(x.people_in_need_id)
                list4.append(x.item_id)
                list5.append(x.quntity)
                list6.append(x.due_date)
                j += 1
                if j == 5:
                    break

            people = zip(list(range(1, j+1)), list3, list4, list5, list6)
            dict = {'role' : role, 'name': name, 'rolenum': rolenum, 'church': church, 'items': items, 'array': array, 'people': people}
        else:
            raise KeyError()
    except:
        dict = {'role' : "Anon", 'name': "", 'rolenum': -1}

    return render(request, "userApp/index.html", dict) 

def onlineDonation(request):
    id = request.COOKIES['userid']
    amount = request.POST['Amount']
    selected_card = request.POST.getlist('card_dropdown')[0]
    church = int(request.POST.getlist('church_dropdown')[0])
    if selected_card == '0':
        if church == 0:
            return HttpResponseRedirect(reverse('index'))

        church = models.Church.objects.get(church_id = church)
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
        if CVV > 999 or CVV < 111:
            return HttpResponseRedirect(reverse('index'))
        
        expiryDate = datetime.strptime(expiryDate, '%Y-%m').date()
        if date.today().year > expiryDate.year:
            return HttpResponseRedirect(reverse('index'))
        if date.today().month > expiryDate.month and date.today().year == expiryDate.year:
            return HttpResponseRedirect(reverse('index'))
        print(save)
        if save == 'on':
            card = models.Card(user_id = models.Donor.objects.get(user_id = id), card_num = cardNumber, cvv = CVV, expiry_date = expiryDate)
            card.save()
    
    # print(datetime.now().strftime('%Y-%m-%d'))
    # print(datetime.now().strftime('%H:%M:%S.%f'))

    reciept = models.Reciept(
                date = datetime.now().strftime('%Y-%m-%d'),
                time = datetime.now().strftime('%H:%M:%S.%f'), 
                user_id = models.Donor.objects.get(user_id = id), 
                church_id = church)

    reciept.save()
    r_details = models.R_Details(
                reciept_id = reciept, item_id = models.Item.objects.get(name = 'Cash'), 
                item_quantity = amount)
    r_details.save()

    all_item_details = models.ItemDetails.objects.all()

    ok = 0

    for x in all_item_details:
        if x.church_id == church and x.item_id == models.Item.objects.get(name = 'Cash'):
            x.quantity += int(amount)
            x.save()
            ok = 1
            break

    if ok == 0:
        item_cash = models.ItemDetails(
                    church_id = church,
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
        reserves = models.Reserves(
                    user_id = models.Donor.objects.get(user_id = id),
                    church_id = models.Church.objects.get(church_id = selected_church),
                    date = meeting_date, 
                    time = selected_timeslot
        )

        reserves.save()

    except:
        return HttpResponseRedirect(reverse('inPersonDonation'))

    return HttpResponseRedirect('/')


def aboutPage(request):
    try:
        y = models.User.objects.get(user_id = request.COOKIES['userid']).role
        role = models.Roles.objects.get(role_number = y).role_name
        name = models.User.objects.get(user_id = request.COOKIES['userid']).name
        state = 1
        dict = {'role' : role, 'name': name, 'state': state, 'rolenum': y}
    except:
        state = 2
        dict = {'role' : "", 'name': "", 'state': state, 'rolenum': -1}
    
    return render(request, "userApp/about.html", dict)