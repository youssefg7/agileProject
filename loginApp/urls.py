from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name='loginPage'),
    path('loginSubmit/', views.loginSubmit, name='loginSubmit'),
]