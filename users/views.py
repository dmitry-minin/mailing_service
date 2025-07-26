from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.conf import settings

from .forms import RegistrationForm
from .models import EmailActivation, CustomUser


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('users:please_confirm')

    def form_valid(self, form):
        # создаём неактивного пользователя
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # добавляем в группу Users
        grp, _ = Group.objects.get_or_create(name='Users')
        user.groups.add(grp)
        # генерируем токен и шлём письмо
        activation = EmailActivation.create_token(user)
        link = self.request.build_absolute_uri(
            reverse_lazy('users:activate', args=[activation.token])
        )
        send_mail(
            'Подтвердите ваш email',
            f'Для активации пройдите по ссылке:\n\n{link}',
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        return super().form_valid(form)


class PleaseConfirmView(TemplateView):
    template_name = 'users/please_confirm.html'


class ActivateView(TemplateView):
    template_name = 'users/activation_invalid.html'

    def get(self, request, token, *args, **kwargs):
        try:
            activation = EmailActivation.objects.get(token=token)
        except EmailActivation.DoesNotExist:
            return super().get(request, *args, **kwargs)

        if activation.is_expired():
            return super().get(request, *args, **kwargs)

        # активируем и логиним
        user = activation.user
        user.is_active = True
        user.save(update_fields=['is_active'])
        # повторно в группу Users (безопасно)
        grp, _ = Group.objects.get_or_create(name='Users')
        user.groups.add(grp)
        login(request, user)
        return redirect('mailings:home')
