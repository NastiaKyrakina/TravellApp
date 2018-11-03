from django.contrib import admin

from HouseSearch.models import House, HousePhoto
from . import models


# Register your models here.

admin.site.register(models.UserInfo)
admin.site.register(models.Note)
admin.site.register(models.Attachment)
admin.site.register(models.Country)
admin.site.register(House)
admin.site.register(HousePhoto)
