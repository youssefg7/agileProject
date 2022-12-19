from django.contrib import admin
from .models import User, Card, Church, Donor, Item, R_Details, Reciept, Reserves, Roles, Servant, UserFavChurch, Admin

# Register your models here.
admin.site.register(User)
admin.site.register(Card)
admin.site.register(Church)
admin.site.register(Donor)
admin.site.register(Item)
admin.site.register(R_Details)
admin.site.register(Reciept)
admin.site.register(Reserves)
admin.site.register(Roles)
admin.site.register(Servant)
admin.site.register(UserFavChurch)
admin.site.register(Admin)