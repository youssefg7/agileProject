from datetime import date, datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from dbApp import models

# Create your views here.

def index(request):
    try:
        id = request.COOKIES['userid']
        rolenum = models.User.objects.get(user_id = id).role
        role = models.Roles.objects.get(role_number = rolenum).role_name
        name = models.User.objects.get(user_id = id).name
        array = [1,2]
        churches = models.Church.objects.all()
        all_cards = models.Card.objects.all()
        cards = []
        for x in all_cards:
            if x.user_id == models.Donor.objects.get(user_id = id):
                cards.append(x)
        dict = {'role' : role, 'name': name, 'rolenum': rolenum, 'array':array, 'churches': churches, 'cards': cards}
    except:
        dict = {'role' : "Anon", 'name': "", 'rolenum': -1}
    
    return render(request, "userApp/index.html", dict) 

def creditCardDonation(request):
    id = request.COOKIES['userid']
    amount = request.POST['Amount']
    church = int(request.POST.getlist('dropdown')[0])
    if church == 0:
        return HttpResponseRedirect(reverse('index'))
    save = request.POST['saveCard']
    cardNumber = int(request.POST['Cardnum'])
    holderName = request.POST['Cardholdname']
    CVV = int(request.POST['CVV'])
    expiryDate = request.POST['Expiry']   
    if cardNumber > 9999999999999999 or cardNumber < 1111111111111111:
        return HttpResponseRedirect(reverse('index'))
    if CVV > 999 or CVV < 111:
        return HttpResponseRedirect(reverse('index'))
    if CVV > 999 or CVV < 111:
        return HttpResponseRedirect(reverse('index'))
    expiryDate = datetime.strptime(expiryDate, '%Y-%m').date()
    print(expiryDate)
    if date.today().year > expiryDate.year:
        return HttpResponseRedirect(reverse('index'))
    if date.today().month > expiryDate.month and date.today().year == expiryDate.year:
        return HttpResponseRedirect(reverse('index'))

    if save == 'on':
        card = models.Card(user_id = models.Donor.objects.get(user_id = id), card_num = cardNumber, cvv = CVV, expiry_date = expiryDate)
        card.save()
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