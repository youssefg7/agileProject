from django.db import models
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
# from viewflow.fields import CompositeKey


class Roles(models.Model):
    role_number = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=254)

class User(models.Model):
    user_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 254)
    email = models.EmailField(max_length = 254, unique = True)
    password = models.CharField(max_length = 32)
    role = models.IntegerField(max_length=254)
    fav_church = models.CharField(max_length = 254, default="")

class Donor(models.Model):
    user_id = models.ForeignKey(User,primary_key = True, on_delete = models.CASCADE)
    
class Card(models.Model):
    user_id = models.ForeignKey(Donor, on_delete = models.CASCADE)
    cvv = models.IntegerField(validators = [MaxValueValidator(999), MinValueValidator(0)])
    card_num = models.IntegerField(validators = [MaxValueValidator(9999999999999999), MinValueValidator(0)], primary_key = True)
    expiry_date = models.DateField()

class Church(models.Model):
    church_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 254)
    address = models.CharField(max_length = 254)

class Item(models.Model):
    item_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 254)
    quantity = models.IntegerField(validators = [MinValueValidator(0)], default = 0)
    church_id = models.ForeignKey(Church, on_delete = models.CASCADE)

class Servant(models.Model):
    user_id = models.OneToOneField(User, primary_key = True, on_delete = models.CASCADE)
    church_id = models.ForeignKey(Church, on_delete = models.CASCADE)

class Reciept(models.Model):
    reciept_id = models.AutoField(primary_key = True)
    date = models.DateField()
    time = models.TimeField()
    user_id = models.ForeignKey(User, on_delete = models.PROTECT)
    church_id = models.ForeignKey(Church, on_delete = models.CASCADE)

class R_Details(models.Model):
    id = models.Field( ('reciept_id','item_id'), primary_key=True, default=(-1, -1)) # I don't know why it's considered an error but it works so ¯\_(ツ)_/¯
    reciept_id = models.ForeignKey(Reciept, on_delete = models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete = models.PROTECT)
    item_quantity = models.IntegerField(validators = [MinValueValidator(0)], default = 0)

class Reserves(models.Model):
    reservation_num = models.AutoField(primary_key = True)
    date = models.DateField()
    time = models.TimeField()
    user_id = models.ForeignKey(Donor, on_delete = models.CASCADE)
    church_id = models.ForeignKey(Church, on_delete = models.CASCADE)

  

# Create your models here.
