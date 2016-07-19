from django import forms
from .models import Sighting

class SightingsForm(forms.ModelForm):
    class Meta:
        model = Sighting
        fields = ('caption','species_tags','lat','lng','sighting_date', 'image', 'location')
        widgets = {
            'caption': forms.TextInput(attrs={'class':"mdl-textfield__input"}),
            'sighting_date': forms.TextInput(attrs={'class':"mdl-textfield__input"}),
            'species_tags': forms.TextInput(attrs={'class':"mdl-textfield__input"}),
            'sighting_date': forms.TextInput(attrs={'class':"mdl-textfield__input"}),
            'location': forms.TextInput(attrs={'class':"mdl-textfield__input"}),
            'lat': forms.HiddenInput(),
            'lng': forms.HiddenInput()
        }