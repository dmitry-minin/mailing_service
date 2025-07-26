from django import forms
from .models import Client, Message, Mailing


class ClientForm(forms.ModelForm):
    """Форма для добавления и редактирования клиента"""

    class Meta:
        model = Client
        fields = ['full_name', 'email', 'comment']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ФИО клиента'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email клиента'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Комментарий (необязательно)',
                'rows': 3
            }),
        }


class MessageForm(forms.ModelForm):
    """Форма для добавления и редактирования сообщения"""

    class Meta:
        model = Message
        fields = ['subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тема письма'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст сообщения',
                'rows': 5
            }),
        }


class MailingForm(forms.ModelForm):
    """Форма для создания и редактирования рассылки"""

    class Meta:
        model = Mailing
        fields = ['start_time', 'end_time', 'message', 'clients']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'message': forms.Select(attrs={'class': 'form-select'}),
            'clients': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
        labels = {
            'start_time': 'Дата и время начала',
            'end_time': 'Дата и время окончания',
            'message': 'Сообщение',
            'clients': 'Клиенты',
        }