from django.db import models
from django.contrib.auth.models import User
from model_utils import Choices
from UserProfile.models import Country

from django.urls import reverse


def get_sentinel_country():
    return Country.objects.get_or_create(name='deleted')[0]


class HouseManager(models.Manager):

    def get_queryset(self):
        return super(HouseManager, self).get_queryset().filter(deleted__isnull=True)

    def multi_search(self, houses, kwargs):

        if 'min_price' in kwargs:
            houses = houses.filter(price__gt=kwargs['min_price'])
        if 'max_price' in kwargs:
            houses = houses.filter(price__lt=kwargs['max_price'])
        if 'country' in kwargs:
            country_id = Country.objects.get(name=kwargs['country']);
            houses = houses.filter(country=country_id)
        if 'type' in kwargs:
            print(kwargs['type'])
            for type in House.HOUSE_TYPE:
                if not (type[0] in kwargs['type']):
                    houses = houses.exclude(type=type[0])

        if 'city' in kwargs:
            houses = houses.filter(city=kwargs['city'])
        if 'rooms' in kwargs:
            houses = houses.filter(rooms=kwargs['rooms'])
        if 'sleeper' in kwargs:
            houses = houses.filter(sleeper=kwargs['sleeper'])
        if 'public' in kwargs:
            houses = houses.filter(date_public__gt=kwargs['public'])
        if 'active' in kwargs:
            if kwargs['active']:
                houses = houses.filter(activity=True)

        return houses


class HouseDeleteManager(models.Manager):

    def get_queryset(self):
        return super(HouseDeleteManager, self).get_queryset().filter(deleted__isnull=False).order_by('-deleted')


MAX_USER_HOUSES = 10
MAX_PRICE = 999.99
MAX_ROOMS = 50
MAX_SLEEPER = 100

class House(models.Model):

    PRIVATE_HOUSE = 'PH'
    APARTMENT = 'AP'
    VILLA = 'VL'

    HOUSE_TYPE = Choices(
        (PRIVATE_HOUSE, 'Private house'),
        (APARTMENT, 'Apartment'),
        (VILLA, 'Villa'),
    )
    """Owner user"""
    owner = models.ForeignKey(User, on_delete='Cascade')

    title = models.CharField(max_length=100, blank=True)

    """Piece of address"""
    country = models.ForeignKey(Country, on_delete=models.SET(get_sentinel_country))
    city = models.CharField(max_length=40)
    address = models.CharField(max_length=100)

    """Describe house"""
    type = models.CharField(max_length=2, choices=HOUSE_TYPE, default=PRIVATE_HOUSE)
    rooms = models.SmallIntegerField(default=1)
    sleeper = models.SmallIntegerField(default=1)
    about = models.TextField(max_length=500)

    price = models.DecimalField(decimal_places=2, max_digits=10)

    activity = models.BooleanField(default=True)
    date_public = models.DateField(auto_now_add=True)
    deleted = models.DateField(null=True, blank=True, db_index=True)

    objects = HouseManager()
    house_delete_objects = HouseDeleteManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('house', args=[str(self.id)])

    def get_images(self):
        return self.housephoto_set.all()

    def main_image(self):
        main_image = self.housephoto_set.first()
        if main_image:
            return main_image.image.url
        return None


class HousePhoto(models.Model):
    house = models.ForeignKey(House, on_delete='Cascade')
    image = models.ImageField(upload_to='house_data/photo/', blank=True)

    def __str__(self):
        return self.image.path
