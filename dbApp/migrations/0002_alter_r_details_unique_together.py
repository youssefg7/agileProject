# Generated by Django 4.1.4 on 2022-12-19 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='r_details',
            unique_together={('reciept_id', 'item_id')},
        ),
    ]
