from django import forms
from HouseSearch.models import House, HousePhoto


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['title', 'country', 'city', 'address', 'type',
                  'rooms', 'sleeper', 'price', 'activity', 'about']

        widgets = {
            'title': forms.TextInput,
            'country': forms.Select,
            'city': forms.TextInput,
            'address': forms.TextInput,
            'type': forms.Select(choices=House.HOUSE_TYPE),
            'rooms': forms.NumberInput,
            'sleeper': forms.NumberInput,

            'about': forms.Textarea,
        }

    def save(self, user):
        house = super(HouseForm, self).save(commit=False)
        house.owner = user
        house.save()
        return house


class PhotoForm(forms.ModelForm):
    class Meta:
        model = HousePhoto
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs=
                                     {'name': 'photo',
                                      'multiple': True,
                                      'required': False,
                                      'accept': 'image/*'})
        }


class SearchHousesForm(forms.Form):
    country = forms.CharField(

    )
    city = forms.CharField()
    type = forms.ChoiceField(
        choices=House.HOUSE_TYPE,
        widget=forms.CheckboxSelectMultiple()
    )
    min_price = forms.DecimalField(
        widget=forms.NumberInput()
    )
    max_price = forms.DecimalField()
    rooms = forms.IntegerField()
    sleeper = forms.IntegerField()
    active = forms.BooleanField(label='Only active')
