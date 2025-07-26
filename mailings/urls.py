from django.urls import path
from .views import (
    HomeView,
    user_toggle_view,
    mailing_toggle_view,
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView,
    MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView,
    MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, MailingLaunchView,
)

app_name = 'mailings'

urlpatterns = [
    # Домашняя страница
    path('', HomeView.as_view(), name='home'),

    # Toggle-операции
    path('users/<int:pk>/toggle/', user_toggle_view, name='user_toggle'),
    path('mailings/<int:pk>/toggle/', mailing_toggle_view, name='mailing_toggle'),
    path('mailings/<int:pk>/launch/', MailingLaunchView.as_view(), name='mailing_launch'),

    # CRUD для клиентов
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client_edit'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    # CRUD для сообщений
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/edit/', MessageUpdateView.as_view(), name='message_edit'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    # CRUD для рассылок
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/edit/', MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
]
