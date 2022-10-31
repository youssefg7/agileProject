# Generated by Django 4.1.2 on 2022-10-30 16:25

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dbApp', '0001_initial'),
    ]

    operations = [
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
        migrations.CreateModel(
            name='Reciept',
            fields=[
                ('reciept_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('church_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbApp.church')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dbApp.user')),
            ],
        ),
        migrations.CreateModel(
            name='R_Details',
            fields=[
                ('item_quantity', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dbApp.item')),
                ('reciept_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbApp.reciept')),
            ],
        ),
    ]