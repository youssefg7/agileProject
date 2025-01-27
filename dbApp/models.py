from django.db import models
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.conf import global_settings
from django.utils import translation


# from viewflow.fields import CompositeKey


class Roles(models.Model):
    role_number = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=254)

class User(models.Model):
    user_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 254)
    email = models.EmailField(max_length = 254, unique = True)
    password = models.CharField(max_length = 32)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)

class Item(models.Model):
    item_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 254)

class Church(models.Model):
    church_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 254)
    address = models.CharField(max_length = 254)
    phone_number = models.CharField(max_length=15, default='Not Available')

class ItemDetails(models.Model):
    church_id = models.ForeignKey(Church, on_delete = models.CASCADE, default=-1)
    item_id = models.ForeignKey(Item, on_delete = models.CASCADE)
    quantity = models.IntegerField(validators = [MinValueValidator(0)], default = 0)

    class Meta:
        ordering = ['-quantity']
        unique_together = ('church_id','item_id')


class PeopleInNeed(models.Model):
    id = models.CharField(max_length=14, primary_key=True)
    name = models.CharField(max_length=254)

class Need(models.Model):
    people_in_need_id = models.ForeignKey(PeopleInNeed, on_delete = models.CASCADE, default=-1)
    item_id = models.ForeignKey(Item, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    due_date = models.DateField(null=True)
    period = models.IntegerField()
    church_id = models.ForeignKey(Church, on_delete = models.CASCADE, default=-1)

    class Meta:
        ordering = ['due_date']
        unique_together = ('people_in_need_id','item_id')

class Donor(models.Model):
    user_id = models.ForeignKey(User, primary_key=True, on_delete = models.CASCADE)
    fav_church = models.ManyToManyField(Church)

class Admin(models.Model):
    user_id = models.ForeignKey(User, primary_key=True, on_delete = models.CASCADE)
    church_id = models.ForeignKey(Church, on_delete = models.CASCADE, default=-1)
    
class Card(models.Model):
    user_id = models.ForeignKey(Donor, on_delete = models.CASCADE)
    cvv = models.IntegerField()
    card_num = models.CharField(primary_key = True, max_length=254)
    expiry_date = models.DateField()


class Reciept(models.Model):
    reciept_id = models.AutoField(primary_key = True)
    date = models.DateField()
    time = models.TimeField()
    user_id = models.ForeignKey(Donor, on_delete = models.PROTECT)
    church_id = models.ForeignKey(Church, on_delete = models.CASCADE)

class RecieptDetails(models.Model):
    reciept_id = models.ForeignKey(Reciept, on_delete = models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete = models.PROTECT)
    item_quantity = models.IntegerField(validators = [MinValueValidator(0)], default = 0)

    class Meta:
        unique_together = ('reciept_id','item_id')
        index_together = ('reciept_id','item_id')


class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key = True)
    date = models.DateField()
    time = models.TimeField()
    user_id = models.ForeignKey(Donor, on_delete = models.CASCADE)
    church_id = models.ForeignKey(Church, on_delete = models.CASCADE)

    class Meta:
        ordering = ['date', 'time']
# Create your models here.
