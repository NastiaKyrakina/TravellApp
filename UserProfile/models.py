from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from model_utils import Choices
from Lib import FFD
from datetime import datetime

class UserExt(User):
    class Meta:
        proxy = True

    def get_new_note_portion(self, since=None, limit=10):
        qs = self.note_set.order_by('-date_public')
        if since:
            qs = qs.filter(date_public__lte=since)
        qs = qs[0:limit]
        return qs

    def get_absolute_url(self):
        return reverse('home', args=[str(self.id)])


class UserInfo(models.Model):

    TRAVEL = 'TR'
    SEARCH = 'SH'
    RENT_HOUSE = 'HH'
    STATUS_TYPE = Choices(
        (TRAVEL, 'Travelling'),
        (SEARCH, 'Find house'),
        (RENT_HOUSE, 'Rent a house'),
    )

    user = models.OneToOneField(User,
                                unique=True,
                                on_delete='Cascade')
    gender = models.BooleanField(default=False)
    birthday = models.DateField(blank=True)
    status = models.CharField(max_length=2,
                              choices=STATUS_TYPE,
                              blank=True,
                              default=TRAVEL)

    phone_num = models.CharField(max_length=12,
                                 blank=True)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30,
                            blank=True)
    info = models.TextField(max_length=256,
                            blank=True)

    registration = models.DateField(auto_now_add=True)
    last_visit = models.DateTimeField(auto_now=True)
    big_photo = models.ImageField(upload_to='user_photo/',
                                  blank=True,
                                  default='def_user_photo.png')


class NoteManager(models.Manager):

    def get_query_set(self):
        return super(NoteManager, self).get_query_set().filter(deleted__isnull=True)


class NoteDeleteManager(models.Manager):

    def get_query_set(self):
        return super(NoteDeleteManager, self).get_query_set().filter(deleted__isnull=False).order_by('-deleted')


class Note(models.Model):

    user = models.ForeignKey(User, on_delete='Cascade')
    text = models.TextField(max_length=1000, blank=True)
    date_public = models.DateTimeField(auto_now_add=True)

    deleted = models.DateField(null=True, db_index=True)

    note_objects = NoteManager()
    objects = NoteManager()
    note_delete_objects = NoteDeleteManager()

    def get_absolute_url(self):
        return reverse('note', args=[str(self.id)])

    def get_images(self):
        return self.attachment_set.filter(type=FFD.IMAGE)

    def get_video(self):
        return self.attachment_set.filter(type=FFD.VIDEO)

    def get_audio(self):
        return self.attachment_set.filter(type=FFD.AUDIO)

    def get_files(self):
        return self.attachment_set.filter(type=FFD.FILES)


def get_upload_file_way(ftype):
    return 'user_files/%s/' % ftype


class Attachment(models.Model):

    note = models.ForeignKey(Note, on_delete='Cascade')
    type = models.CharField(max_length=2,
                            choices=FFD.FILE_TYPE)
    file = models.FileField(upload_to='user_files/all_files/',
                            blank=True)


def save_attach(files_dict, note):
    files = files_dict.getlist('images', None)
    for file in files:
        new_attachment = Attachment(note=note, file=file, type='IM')
        new_attachment.save()

    files = files_dict.getlist('video', None)
    for file in files:
        new_attachment = Attachment(note=note, file=file, type='VD')
        new_attachment.save()

    files = files_dict.getlist('audio', None)
    for file in files:
        new_attachment = Attachment(note=note, file=file, type='AU')
        new_attachment.save()

    files = files_dict.getlist('files', None)
    for file in files:
        new_attachment = Attachment(note=note, file=file, type='FL')
        new_attachment.save()
