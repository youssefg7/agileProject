# Generated by Django 4.1.4 on 2022-12-21 01:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dbApp', '0015_alter_need_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeopleInNeed',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=254)),
                ('chuch_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbApp.church')),
            ],
        ),
        migrations.AddField(
            model_name='need',
            name='people_in_need_id',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='dbApp.peopleinneed'),
        ),
        migrations.AlterUniqueTogether(
            name='need',
            unique_together={('people_in_need_id', 'item_id')},
        ),
    ]