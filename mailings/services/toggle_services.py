from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from mailings.models import Mailing


User = get_user_model()


def toggle_user_active(user_pk):
    """
    Переключает статус активности пользователя между True и False.
    """
    user = User.objects.get(pk=user_pk)
    user.is_active = not user.is_active
    user.save(update_fields=['is_active'])
    return user.is_active


def toggle_mailing_active(pk):
    """
    Переключает статус рассылки между 'started'/'completed' и 'created'.
    Если рассылка завершена ('completed'), переводит в 'created'.
    Если рассылка в процессе ('started' или 'created'), переводит в 'completed'.
    """
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.status in ['started', 'created']:
        mailing.status = 'completed'
    else:  # status is 'completed'
        mailing.status = 'created'
    mailing.save()
