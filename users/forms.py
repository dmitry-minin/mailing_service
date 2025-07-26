from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegistrationForm(UserCreationForm):
    """ Форма регистрации пользователя по email и паролю. """
    email = forms.EmailField(label='Email', required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')
