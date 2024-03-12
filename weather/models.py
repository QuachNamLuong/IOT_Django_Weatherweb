from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput, PasswordInput

class City(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=100,  default='')

    def __str__(self): #show the actual city name on the dashboard
        return self.name

    class Meta: 
        verbose_name_plural = 'cities'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1', 'password2']
        widgets = {
            'username': TextInput(attrs={'placeholder' : 'username'}),
        }
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
        self.fields['password2'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'})
