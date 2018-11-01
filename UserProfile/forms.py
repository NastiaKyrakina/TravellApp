from django import forms

from UserProfile.models import *


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ['user', 'date_public', 'deleted']

        widgets = {
            'text': forms.Textarea(attrs={'class': 'full'}),
        }


class AttachmentForm(forms.Form):
    images = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'name': 'photo',
                                      'multiple': True,
                                      'required': False,
                                      'accept': 'image/*'})
    )

    video = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'name': 'video',
                                      'multiple': True,

                                      'required': False,
                                      'accept': 'video/*'})
    )

    audio = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'name': 'audio',
                                      'multiple': True,
                                      'required': False,
                                      'accept': 'audio/*'})
    )

    files = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'name': 'files',
                                      'required': False,
                                      'multiple': True,
                                      })
    )
