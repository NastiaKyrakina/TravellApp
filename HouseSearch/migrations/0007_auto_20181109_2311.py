# Generated by Django 2.1.2 on 2018-11-09 23:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('HouseSearch', '0006_auto_20181109_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='correct',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='rate',
            name='date_public',
            field=models.DateField(auto_now=True),
        ),
    ]
