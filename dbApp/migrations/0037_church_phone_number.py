# Generated by Django 4.1.4 on 2022-12-31 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbApp', '0036_alter_reservation_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='church',
            name='phone_number',
            field=models.CharField(default='Not Available', max_length=15),
        ),
    ]
