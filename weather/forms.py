from django import forms
from django.forms import  ModelForm, TextInput
from .models import City

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name', 'username']
        widgets = {
            'name': TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'}),
            'username': TextInput(attrs={'placeholder' : 'Username', 'class': 'hidden-username', 'value': '{{username}}'}),
        }
