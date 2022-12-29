from django.contrib import admin
from .models import PeopleInNeed, Need, User, Card, ItemDetails, Church, Donor, Item, RecieptDetails, Reciept, Reservation, Roles, Admin

# Register your models here.
admin.site.register(User)
admin.site.register(Card)
admin.site.register(Church)
admin.site.register(Donor)
admin.site.register(Item)
admin.site.register(RecieptDetails)
admin.site.register(Reciept)
admin.site.register(Reservation)
admin.site.register(Roles)
admin.site.register(Admin)
admin.site.register(ItemDetails)
admin.site.register(PeopleInNeed)
admin.site.register(Need)
