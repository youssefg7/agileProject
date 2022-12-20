from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.aboutPage, name="about"),
    path('creditCardDonation/', views.creditCardDonation, name='creditCardDonation'),
]
