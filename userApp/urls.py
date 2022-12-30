from django.urls import path
from . import views

app_name = 'userApp'

urlpatterns = [
    path('', views.index, name="index"),
    path("about/", views.aboutPage, name="aboutPage"),
    path('onlineDonation/', views.onlineDonation, name='onlineDonation'),
    path('inPersonDonation/', views.inPersonDonation, name='inPersonDonation'),
    path('adminInv/', views.adminInvPage, name='adminInvPage'),
    path('adminPeopleIN/', views.adminPeopleINPage, name='adminPeopleIN'),
    path('adminReservation/', views.adminReservation, name='adminReservation'),
    path('Giveout/', views.Giveout, name='Giveout'),
    path('myAccountSubmit/', views.myAccountSubmit, name='myAccountSubmit'),
    path('addAdminSubmit/', views.addAdminSubmit, name='addAdminSubmit'),
    path('addpeopleinneedSubmit/', views.addpeopleinneedSubmit, name='addpeopleinneedSubmit'),
    path('inventorySubmit/', views.inventorySubmit, name='inventorySubmit'),
    path('Myaccount/', views.myAccount, name='myAccount'),
]
