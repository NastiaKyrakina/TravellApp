# Generated by Django 2.1.2 on 2018-11-09 23:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('HouseSearch', '0005_auto_20181102_1851'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=1, max_digits=2)),
                ('comment', models.TextField(max_length=1000)),
                ('house', models.ForeignKey(on_delete='Cascade', to='HouseSearch.House')),
                ('user', models.ForeignKey(on_delete='Cascade', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='housephoto',
            name='image',
            field=models.ImageField(blank=True, upload_to='house_data/photo/'),
        ),
    ]
