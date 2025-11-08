from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Participant

class CustomUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=False)

    class Meta:
        model = Participant
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ''
    }))
    password = forms.CharField(
        label='',widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': ''
    }))