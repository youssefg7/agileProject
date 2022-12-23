# Generated by Django 4.1.4 on 2022-12-23 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dbApp', '0022_remove_timeslots_church_id_delete_reserves_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timeslots',
            fields=[
                ('time_id', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.TimeField()),
                ('church_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbApp.church')),
            ],
        ),
        migrations.CreateModel(
            name='Reserves',
            fields=[
                ('reservation_num', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('church_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbApp.church')),
                ('time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbApp.timeslots')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbApp.donor')),
            ],
        ),
    ]
