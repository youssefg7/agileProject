from django.urls import path
from . import views

app_name = 'userApp'


urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.aboutPage, name="about"),
    path('creditCardDonation/', views.creditCardDonation, name='creditCardDonation'),
<<<<<<< HEAD
    path('inPersonDonation/', views.inPersonDonation, name='inPersonDonation'),
=======
    path('adminInv/', views.adminInvPage, name='adminInvPage'),
    path('adminPeopleIN/', views.adminPeopleINPage, name='adminPeopleIN'),

>>>>>>> 2bcd48137d6921e30e19b647fe012f9c5953ccd2
]
