# Generated by Django 4.1.4 on 2022-12-21 01:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbApp', '0017_alter_need_due_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='peopleinneed',
            name='chuch_id',
        ),
    ]
