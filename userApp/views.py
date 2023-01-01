from datetime import datetime
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from dbApp import models
from Util import *
import reportlab 
from reportlab.pdfgen import canvas

# Render the inventory dashboard
def adminInvPage(request):
    clearAlert(request)
    try:
        # Get stored data needed for inventory dashborad
        id = getId(request)
        user = getUser(id)
        church = getAdminChurch(id)
        all_items = getItemDetailsFiltered(church)
        l = len(all_items)
        items = zip(list(range(1, l+1)), all_items)
        dict = {'user':user, 'church': church, 'items': items, 'sz': l}
    except:
        return redirect('userApp:index')
    return render(request, "userApp/admininv.html",dict)

# Render people in need dashboadrd
def adminPeopleINPage(request):
    request.session['print'] = 1
    clearAlert(request)
    try:
        # Get stored data needed for people in need dashborad
        id = getId(request)
        user = getUser(id)
        church = getAdminChurch(id)
        all_needs = getNeedsFiltered(church)
        l = len(all_needs)
        needs = zip(list(range(1, l+1)), all_needs)
        today = datetime.today().date()
        dict = {'user':user, 'church': church, 'needs': needs, 'today':today, 'sz': l}
    except:
        return redirect('userApp:index')
    return render(request, "userApp/adminPeopleIN.html",dict)

# Render reservation dashboard
def adminReservation(request):
    clearAlert(request)
    try:
        # Get stored data needed for reservation dashborad
        id = getId(request)
        user = getUser(id)
        church = getAdminChurch(id)
        all_reservations = getAllReservationsFiltered(church)
        l = len(all_reservations)
        reservations = zip(list(range(1, l+1)), all_reservations)
        today = datetime.today().date()
        dict = {'user':user, 'church': church, 'reservations': reservations, 'today':today, 'sz': l}
    except:
        return redirect('userApp:index')
    return render(request, "userApp/adminreservation.html",dict)

# Render home page
def index(request):
    clearAlert(request)
    try:
        if request.session['print'] == 1:
            request.session['print'] = 0
            response = HttpResponse(content_type='application/pdf') 

        # This line force a download
            response['Content-Disposition'] = 'attachment; filename="1.pdf"' 


            # Generate unique timestamp
            ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')

            p = canvas.Canvas(response)

            # Write content on the PDF 
            p.drawString(100, 600, "Hello " + " Antooz - " + ts ) 

            # Close the PDF object. 
            p.showPage() 
            p.save() 

            # Show the result to the user    
            return response
    except:
        pass
    try:
        id = getId(request)
        user = getUser(id)
        # Get data needed for Donor home page
        if user.role.role_name == 'Donor':
            churches = getAllChurches()
            cards = getCardsFiltered(id)
            ts = getAllTimeSlots(30)
            dict = {'user':user, 'churches': churches, 'cards': cards, 'timeslots': ts}

        # Get data needed for Admin home page
        elif user.role.role_name == 'Admin':
            church = getAdminChurch(id)
            today = datetime.today().date()
            all_items = getItemDetailsFiltered(church)
            all_needs = getNeedsFiltered(church)
            all_reservations = getAllReservationsFiltered(church)
            items = zip(list(range(1, min(5, len(all_items)) + 1)), all_items)
            needs = zip(list(range(1, min(5, len(all_needs)) + 1)), all_needs)
            reservations = zip(list(range(1, min(5, len(all_reservations)) + 1)), all_reservations)
            dict = {'user':user, 'church': church, 'items': items,'needs': needs, 'reservations': reservations, 'today': today, 'sz1': len(all_needs), 'sz2': len(all_items), 'sz3': len(all_reservations)}
        else:
            raise KeyError()
    except:
        dict = {'role' : "Anon", 'name': "", 'rolenum': -1}
    return render(request, "userApp/index.html", dict) 

# Action taken when giveout button is clicked in people in need dashboard
def Giveout(request):
    selected_need = request.POST.get('Giveout')
    need = models.Need.objects.get(id = selected_need)
    church = need.church_id
    item = need.item_id
    if not saveItemDetailsGiveout(church, item, need):
        makeAlert(request, 1, "Can't Giveout This Item")
        return redirect('userApp:adminPeopleIN')
    needDueDateAlter(need)
    makeAlert(request, 2, "Giveout Done")
    return redirect('userApp:index')

# Donor online cash donation
def onlineDonation(request):
    id = getId(request)
    amount = request.POST['Amount']
    selected_card = request.POST.get('card_dropdown')
    church = int(request.POST.get('church_dropdown'))
    # Error not selecting a church
    if church == 0:
        makeAlert(request, 1, "Please Select a Church")
        return redirect('userApp:index')
    # Use new card
    if selected_card == '0':
        # Get data from view
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
        # Chech credentials
        if not checkOnlineDonation(cardNumber, CVV, expiryDate):
            # Credentials Error
            makeAlert(request, 1, "Enter Valid Card Info")
            return redirect('userApp:index')
        # Save card
        if save == 'on':
            saveCard(id, cardNumber, CVV, expiryDate)
    # Prepare data to be stored
    amount = toInt(amount)
    item = getItemByName('Cash')
    donor = getDonor(id)
    # Store data in database
    saveReciept(donor, church, item, amount)
    saveItemDetails(church, item, amount)
    makeAlert(request, 2, "Donation Done")
    return redirect('userApp:index')

# Reserve in-person meeting for donation
def inPersonDonation(request):
    id = request.COOKIES['userid']
    # Get data from view
    selected_church = int(request.POST.get('church_dropdown2'))
    selected_timeslot = request.POST.get('timeslot_dropdown')
    meeting_date = request.POST['meeting_date']
    # No timeslot seleceted
    if selected_timeslot == '0':
        makeAlert(request, 1, 'Please select a timeslot')
        return redirect('userApp:index')
    # Try to save reservation
    ret = saveReservation(id, selected_church, meeting_date, selected_timeslot)
    # Reservation Error
    if ret != 0:
        # No church selected error
        if ret == 1:
            makeAlert(request, 1, "Please Select a church")
        # No date selected error
        if ret == 2:
            makeAlert(request, 1, "Plase Select Appropriate Date")
        # Already reserved date and time for the church error
        if ret == 3:
            makeAlert(request, 1, "Already Reserved")
        return redirect('userApp:index')
    # Reservation completed
    makeAlert(request, 2, "Reservation Done")  
    return redirect('userApp:index')


def myAccount(request):
    clearAlert(request)
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
    return render(request, "userApp/Myaccount.html", dict)

def myAccountSubmit(request):
    id = getId(request)
    user = getUser(id)
    name = request.POST['Name']
    password = request.POST['Password']
    if name != '':
        user.name = name
    if password != '':
        user.password = password
    user.save()
    if user.role.role_number == 1:
        admin = getAdmin(user)
        church = request.POST.get('church_dropdown')
        if church != '0':
            admin.church_id = getChurch(church)
        admin.save()
    return HttpResponseRedirect('/')

def addAdminSubmit(request):
    id = getId(request)
    email = request.POST['Email']
    emails = getAllEmailsFiltered(email)
    if len(emails) > 0:
        makeAlert(request, 1, 'Email is registered before')
        return redirect('userApp:myAccount')
    name = request.POST['Name']
    church = getAdminChurch(id)
    saveUser(name, email, 'Admin', 'Admin', church)
    return HttpResponseRedirect('/')

def addpeopleinneedSubmit(request):
    id = getId(request)
    person = request.POST.get('people_dropdown')
    item = request.POST['item_datalist1']
    quantity = request.POST['Quantity1']
    period = request.POST['Period']
    date = request.POST['due_date']
    church = getAdminChurch(id)
    if person == '-1':
        name = request.POST['person_name']
        ID = request.POST['person_ID']
        if name == '':
            makeAlert(request, 1, 'Specify Person in Need Name')
            return redirect('userApp:myAccount')
        if ID == '':
            makeAlert(request, 1, 'Specify Person in Need National ID')
            return redirect('userApp:myAccount')
        person = models.PeopleInNeed(id = ID, name = name)
        person.save()
    elif person == '0':
        makeAlert(request, 1, 'Please Choose a Person in Need or Add New One')
        return redirect('userApp:myAccount')
    else:
        person = getPeopleInNeed(person)
    if date == '':
        makeAlert(request, 1, 'Specify a Date')
        return redirect('userApp:myAccount')
    if item == '':
        makeAlert(request, 1, 'Specify an Item')
        return redirect('userApp:myAccount')
    if quantity == '':
        makeAlert(request, 1, 'Specify a Quantity')
        return redirect('userApp:myAccount')
    if period == '':
        makeAlert(request, 1, 'Specify a Period')
        return redirect('userApp:myAccount')
    date = datetime.strptime(date, '%Y-%m-%d').date()
    item = getItemByName(item)
    changeSaveNeed(church, item, person, quantity, date, period)
    return HttpResponseRedirect('/')

def inventorySubmit(request):
    id = getId(request)
    donor = request.POST.get('donor_dropdown')
    item = request.POST['item_datalist2']
    quantity = request.POST['Quantity2']
    church = getAdminChurch(id)
    if donor == '-1':
        name = request.POST['donor_name']
        email = request.POST['donor_email']
        if name == '':
            makeAlert(request, 1, 'Specify Donor Name')
            return redirect('userApp:myAccount')
        if email == '':
            makeAlert(request, 1, 'Specify Donor Email')
            return redirect('userApp:myAccount')
        donor = saveUser(name, email, 'Donor', 'Donor')
    elif donor == '0':
        makeAlert(request, 1, 'Please Choose a Donor or Add New One')
        return redirect('userApp:myAccount')
    else:
        donor = getDonor(donor)
    if item == '':
        makeAlert(request, 1, 'Specify an Item')
        return redirect('userApp:myAccount')
    if quantity == '':
        makeAlert(request, 1, 'Specify a Quantity')
        return redirect('userApp:myAccount')
    quantity = toInt(quantity)
    item = getItemByName(item)
    saveReciept(donor, church, item, quantity)
    saveItemDetails(church, item, quantity)
    return HttpResponseRedirect('')

def knesetyChurches(request):
    clearAlert(request)
    all_churches = getAllChurches()
    l = len(all_churches)
    churches = zip(range(1, l + 1), all_churches)
    try:
        id = getId(request)
        user = getUser(id)
        dict = {'user':user, 'churches':churches, 'sz': l}
    except:
        dict = {'churches':churches, 'sz': l}
    return render(request, "userApp/kenestychurches.html", dict)