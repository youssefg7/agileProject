from datetime import date, datetime
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
        all_items = models.ItemDetails.objects.all()
        list1 = []
        list2 = []
        i = 0
        for x in all_items:
            if x.church_id == church:    
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
        all_needs = models.Need.objects.all()

        list1 = []
        list2 = []
        list3 = []
        list4 = []
        i = 0
        for x in all_needs:
            print(x)
            if x.chuch_id == church:    
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

def index(request):
    try:
        id = request.COOKIES['userid']
        rolenum = models.User.objects.get(user_id = id).role
        role = models.Roles.objects.get(role_number = rolenum).role_name
        name = models.User.objects.get(user_id = id).name
        array = [1,2]
        if rolenum == 2:
            churches = models.Church.objects.all()
            cards = []
            all_cards = models.Card.objects.all()
            for x in all_cards:
                if x.user_id == models.Donor.objects.get(user_id = id):
                    cards.append(x)
            dict = {'role' : role, 'name': name, 'rolenum': rolenum, 'array': array, 'churches': churches, 'cards': cards}
        elif rolenum == 1:
            church = models.Admin.objects.get(user_id = id)
            church = church.church_id
            all_items = models.ItemDetails.objects.all()
            list1 = []
            list2 = []
            i = 0
            for x in all_items:
                if x.church_id == church:    
                    list1.append(x.item_id)
                    list2.append(x.quantity)
                    i += 1
                if i == 5:
                    break
            items = zip(list(range(1, i+1)), list1, list2)

            all_needs = models.Need.objects.all()

            list3 = []
            list4 = []
            list5 = []
            list6 = []
            j = 0
            for x in all_needs:
                if x.chuch_id == church:    
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

def creditCardDonation(request):
    id = request.COOKIES['userid']
    amount = request.POST['Amount']
    selected_card = request.POST.get('saved_card').getlist('card_dropdown')
    church = int(request.POST.getlist('church_dropdown')[0])
    print(selected_card)
    print(church)
    # if selected_card == 0:
    #     if church == 0:
    #         return HttpResponseRedirect(reverse('index'))

    #     church = models.Church.objects.get(church_id = church)
    #     cardNumber = request.POST['Cardnum']
    #     holderName = request.POST['Cardholdname']
    #     CVV = int(request.POST['CVV'])
        
    #     try:
    #         save = request.POST['saveCard']
    #     except:
    #         save = ''
        
    #     expiryDate = request.POST['Expiry']   
    #     if cardNumber > '9999999999999999' or cardNumber < '1000000000000000':
    #         return HttpResponseRedirect(reverse('index'))
    #     if CVV > 999 or CVV < 111:
    #         return HttpResponseRedirect(reverse('index'))
        
    #     expiryDate = datetime.strptime(expiryDate, '%Y-%m').date()
    #     # print(expiryDate)
    #     if date.today().year > expiryDate.year:
    #         return HttpResponseRedirect(reverse('index'))
    #     if date.today().month > expiryDate.month and date.today().year == expiryDate.year:
    #         return HttpResponseRedirect(reverse('index'))

    #     donor_user = models.Donor.objects.get(user_id = id)
    
    #     # print(save)
    #     if save == 'on':
    #         card = models.Card(user_id = donor_user, card_num = cardNumber, cvv = CVV, expiry_date = expiryDate)
    #         card.save()
    
    # # print(datetime.now().strftime('%Y-%m-%d'))
    # # print(datetime.now().strftime('%H:%M:%S.%f'))

    # reciept = models.Reciept(date = datetime.now().strftime('%Y-%m-%d'), time = datetime.now().strftime('%H:%M:%S.%f'), user_id = donor_user, church_id = church)
    # reciept.save()
    # r_details = models.R_Details(reciept_id = reciept.reciept_id, item_id = models.Item.objects.get(name = 'Cash'), item_quantity = amount)
    # r_details.save()
    
    return HttpResponseRedirect('/')

def inPersonDonation(request):
    return HttpResponseRedirect('')



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