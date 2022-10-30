# Generated by Django 4.1.2 on 2022-10-30 16:09

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
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=254)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='dbApp.user')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=254)),
                ('quantity', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('church_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbApp.church')),
            ],
        ),
        migrations.CreateModel(
            name='Servant',
            fields=[
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='dbApp.user')),
                ('church_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbApp.church')),
            ],
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
