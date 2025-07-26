from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from mailings.models import Client, Message, Mailing, MailingAttempt


User = get_user_model()


def get_anonymous_context():
    """
    Контекст для неавторизованного: общие счётчики.
    - общее количество сообщений,
    - общее количество рассылок,
    - общее количество пользователей,
    - общее количество успешно отправленных сообщений.
    """
    return {
        'role': 'anonymous',
        'total_messages': Message.objects.count(),
        'total_mailings': Mailing.objects.count(),
        'total_users': User.objects.count(),
        'total_sent_messages': MailingAttempt.objects.filter(status='success').count(),
    }


def get_user_context(user):
    """
    Контекст для обычного пользователя:
    - его клиенты и рассылки,
    - успех/неудача попыток,
    - общее количество отправленных сообщений.
    """
    clients_qs = Client.objects.filter(owner=user)
    mailings_qs = Mailing.objects.filter(owner=user)
    totals = MailingAttempt.objects.filter(mailing__owner=user).aggregate(
        success=Count('pk', filter=Q(status='success')),
        fail=Count('pk', filter=Q(status='fail')),
    )
    return {
        'role': 'user',
        'clients_list': clients_qs,
        'clients_count': clients_qs.count(),
        'mailings_list': mailings_qs,
        'mailings_count': mailings_qs.count(),
        'attempts_success': totals.get('success', 0),
        'attempts_fail': totals.get('fail', 0),
        'total_sent_messages': totals.get('success', 0),
    }


def get_manager_context(current_user=None):
    """
    Контекст для менеджера:
    - все пользователи (кроме самого менеджера),
    - количество клиентов,
    - все рассылки (для переключения статусов),
    - общая статистика по отправленным сообщениям.
    - Кеширование на 15 минут.
    """

    users_qs = User.objects.all()
    if current_user:
        users_qs = users_qs.exclude(pk=current_user.pk)

    mailings_qs = Mailing.objects.all()
    total_sent = MailingAttempt.objects.filter(status='success').count()

    context = {
        'role': 'manager',
        'users_list': users_qs,
        'users_count': users_qs.count(),
        'clients_count': Client.objects.count(),
        'mailings_list': mailings_qs,
        'mailings_count': mailings_qs.count(),
        'total_sent_messages': total_sent,
    }

    return context
