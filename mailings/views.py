from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
)

from .models import Client, Message, Mailing
from .forms import ClientForm, MessageForm, MailingForm

from mailings.services.home_services import (
    get_anonymous_context, get_user_context, get_manager_context
)
from mailings.services.toggle_services import (
    toggle_user_active, toggle_mailing_active
)
from .services.mailing_services import process_mailing

from django.contrib import messages

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


CACHE_TTL = 60 * 15


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ClientListView(LoginRequiredMixin, ListView):
    """
    Список клиентов.
    - Если пользователь в группе Managers, показываем всех клиентов.
    - Иначе показываем только своих клиентов.
    """
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Managers').exists():
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='Managers').exists()
        return context


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'clients/client_detail.html'
    context_object_name = 'client'

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('mailings:client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('mailings:client_list')

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('mailings:client_list')

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class MessageListView(LoginRequiredMixin, ListView):
    """
    Список сообщений.
    - Если пользователь в группе Managers, показываем все сообщения.
    - Иначе показываем только свои сообщения.
    """
    model = Message
    template_name = 'messages/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Managers').exists():
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='Managers').exists()
        return context


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'messages/message_detail.html'
    context_object_name = 'message'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'messages/message_form.html'
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'messages/message_form.html'
    success_url = reverse_lazy('mailings:message_list')

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'messages/message_confirm_delete.html'
    success_url = reverse_lazy('mailings:message_list')

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class MailingListView(LoginRequiredMixin, ListView):
    """
    Список рассылок.
    - Если пользователь в группе Managers, показываем все рассылки.
    - Иначе показываем только свои рассылки.
    """
    model = Mailing
    template_name = 'mailings/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Managers').exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = self.request.user.groups.filter(name='Managers').exists()
        return context


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingLaunchView(LoginRequiredMixin, View):
    """
    Представление для ручного запуска рассылки
    """

    def post(self, request, *args, **kwargs):
        try:
            # Пытаемся получить рассылку
            mailing = Mailing.objects.filter(
                pk=self.kwargs['pk'],
                owner=request.user
            ).first()

            if not mailing:
                messages.error(request, 'Рассылка не найдена или у вас нет прав на её запуск')
                return redirect('mailings:mailing_list')

            success, message = process_mailing(mailing.pk)

            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)

        except Exception as e:
            messages.error(request, f'Произошла ошибка: {str(e)}')

        return redirect(request.META.get('HTTP_REFERER', 'mailings:mailing_list'))


class HomeView(TemplateView):
    """
    Единая точка входа:
    - anonymous → общая статистика,
    - user      → свои данные,
    - manager   → все данные + кнопки toggle.
    """
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            ctx = get_anonymous_context()
        elif user.groups.filter(name='Managers').exists():
            ctx = get_manager_context(current_user=user)
        else:
            ctx = get_user_context(user)

        ctx['links'] = {
            'clients': 'mailings:client_list',
            'messages': 'mailings:message_list',
            'mailings': 'mailings:mailing_list',
            'home': 'mailings:home',
            'user_toggle': 'mailings:user_toggle',
            'mailing_toggle': 'mailings:mailing_toggle',
        }
        return render(request, self.template_name, ctx)


@login_required
@permission_required('users.change_customuser', raise_exception=True)
def user_toggle_view(request, pk):
    """
    Блокировка/разблокировка аккаунта сервиса (CustomUser).
    Доступно менеджерам с правом users.change_customuser.
    """
    toggle_user_active(pk)
    return redirect(reverse('mailings:home'))


@login_required
@permission_required('mailings.change_mailing', raise_exception=True)
def mailing_toggle_view(request, pk):
    """
    Включение/отключение рассылки (Mailing).
    Доступно менеджерам с правом mailings.change_mailing.
    """
    toggle_mailing_active(pk)
    return redirect(reverse('mailings:home'))
