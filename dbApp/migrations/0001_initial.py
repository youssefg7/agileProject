# Generated by Django 4.1.4 on 2022-12-19 17:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Church',
            fields=[
                ('church_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=254)),
                ('address', models.CharField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='ItemDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbApp.item')),
            ],
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('role_number', models.AutoField(primary_key=True, serialize=False)),
                ('role_name', models.CharField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=254)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=32)),
                ('role', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='dbApp.user')),
                ('church', models.CharField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='dbApp.user')),
            ],
        ),
        migrations.CreateModel(
            name='Reciept',
            fields=[
                ('reciept_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('church_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbApp.church')),
                ('items', models.ManyToManyField(to='dbApp.itemdetails')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dbApp.user')),
            ],
        ),
        migrations.CreateModel(
            name='R_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_quantity', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dbApp.item')),
                ('reciept_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbApp.reciept')),
            ],
        ),
        migrations.AddField(
            model_name='church',
            name='items',
            field=models.ManyToManyField(to='dbApp.itemdetails'),
        ),
        migrations.CreateModel(
            name='Servant',
            fields=[
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='dbApp.user')),
                ('church_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbApp.church')),
            ],
        ),
        migrations.CreateModel(
            name='Reserves',
            fields=[
                ('reservation_num', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('church_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbApp.church')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbApp.donor')),
            ],
        ),
        migrations.AddField(
            model_name='donor',
            name='fav_church',
            field=models.ManyToManyField(to='dbApp.church'),
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('cvv', models.IntegerField(validators=[django.core.validators.MaxValueValidator(999), django.core.validators.MinValueValidator(0)])),
                ('card_num', models.IntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MaxValueValidator(9999999999999999), django.core.validators.MinValueValidator(0)])),
                ('expiry_date', models.DateField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbApp.donor')),
            ],
        ),
    ]
