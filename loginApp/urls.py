from django.urls import path
from . import views

urlpatterns = [
    path('', views.donorLoginPage, name='donorLoginPage'),
    path('donorLoginSubmit/', views.donorLoginSubmit, name='donorLoginSubmit'),
    path('donorMyaccount/', views.myaccountPage, name='donorMyaccount'),
    path('donorSignup/', views.donorSignupPage, name='donorSignup'),
    path('donorLogout/', views.donorLogout, name='donorLogout'),
]