# django forms method needed to alter their database
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

# Meta class for additional data for user
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
