# Generated by Django 4.1.4 on 2022-12-23 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbApp', '0021_alter_itemdetails_index_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslots',
            name='church_id',
        ),
        migrations.DeleteModel(
            name='Reserves',
        ),
        migrations.DeleteModel(
            name='Timeslots',
        ),
    ]
