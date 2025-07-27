from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from mailings.models import Mailing
from users.models import CustomUser
from django.core.cache import cache

User = get_user_model()


def toggle_user_active(user_pk: int):
    """
    Переключает статус активности пользователя между True и False.
    Если пользователь активен, делает его неактивным, и наоборот.
    После изменения статуса сбрасывает кэш для всех дашбордов пользователя и менедж
    """
    user = get_object_or_404(CustomUser, pk=user_pk)

    if user == CustomUser.objects.get(pk=user_pk) and user.has_perm('mailings.block_user'):
        return

    user.is_active = not user.is_active
    user.save(update_fields=['is_active'])

    # очистка всего кэша, чтобы дашборды пересчитались
    cache.clear()


def toggle_mailing_active(mailing_pk: int):
    """
    Переключить статус рассылки:
    created / started  -> completed
    completed          -> created
    После изменения инвалидируем кеш дашбордов.
    """
    mailing = get_object_or_404(Mailing, pk=mailing_pk)

    if mailing.status in ('started', 'created'):
        mailing.status = 'completed'
    else:
        mailing.status = 'created'

    mailing.save(update_fields=['status'])

    # очистка кеша (чтобы на главной сразу обновилось)
    cache.clear()
