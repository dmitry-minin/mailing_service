from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegistrationForm(UserCreationForm):
    """ Форма регистрации пользователя по email и паролю. """
    email = forms.EmailField(label='Email', required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'avatar', 'phone', 'country')
        labels = {
            'email': 'Email',
            'avatar': 'Аватар',
            'phone': 'Телефон',
            'country': 'Страна',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }