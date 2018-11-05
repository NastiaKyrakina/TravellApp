# Generated by Django 2.1.2 on 2018-11-02 17:13

import HouseSearch.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UserProfile', '0011_userinfo_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=40)),
                ('address', models.CharField(max_length=100)),
                ('type',
                 models.CharField(choices=[('PH', 'Private house'), ('AP', 'Apartment'), ('VL', 'Villa')], default='PH',
                                  max_length=2)),
                ('rooms', models.SmallIntegerField(default=1)),
                ('sleeper', models.SmallIntegerField(default=1)),
                ('about', models.TextField(max_length=500)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('activity', models.BooleanField(default=True)),
                ('date_public', models.DateField(auto_now_add=True)),
                ('deleted', models.DateField(db_index=True, null=True)),
                ('country', models.ForeignKey(on_delete=models.SET(HouseSearch.models.get_sentinel_country),
                                              to='UserProfile.Country')),
                ('owner', models.ForeignKey(on_delete='Cascade', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HousePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='house_data/photo/')),
                ('house', models.ForeignKey(on_delete='Cascade', to='HouseSearch.House')),
            ],
        ),
    ]