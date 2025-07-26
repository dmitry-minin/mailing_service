from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import transaction

from mailings.models import Mailing, MailingAttempt


def send_single_mailing(mailing):
    """
    Отправляет одну рассылку всем клиентам
    Возвращает кортеж (успешных_отправок, всего_отправок)
    """
    if not mailing.clients.exists():
        return 0, 0

    success_count = 0
    clients = list(mailing.clients.all())
    
    for client in clients:
        try:
            send_mail(
                mailing.message.subject,
                mailing.message.body,
                settings.EMAIL_HOST_USER,
                [client.email],
                fail_silently=False,
            )
            status = 'success'
            server_response = 'OK'
            success_count += 1
        except Exception as e:
            status = 'fail'
            server_response = str(e)

        # Создаем запись о попытке
        MailingAttempt.objects.create(
            mailing=mailing,
            status=status,
            server_response=server_response
        )
    
    return success_count, len(clients)


def process_mailing(pk):
    """
    Обрабатывает рассылку по ID
    Возвращает кортеж (успех, сообщение)
    """
    try:
        with transaction.atomic():
            mailing = Mailing.objects.select_for_update().get(pk=pk)
            now = timezone.now()
            
            # Проверяем, что время рассылки актуально
            if now > mailing.end_time:
                mailing.status = 'completed'
                mailing.save(update_fields=['status'])
                return False, 'Время рассылки истекло'
                
            if now < mailing.start_time:
                return False, 'Время рассылки еще не наступило'
            
            # Если рассылка в статусе 'created', обновляем на 'started'
            if mailing.status == 'created':
                mailing.status = 'started'
                mailing.save(update_fields=['status'])
            
            # Отправляем письма
            success_count, total = send_single_mailing(mailing)
            
            # Не меняем статус на 'completed', оставляем 'started'
            return True, f'Успешно отправлено {success_count} из {total} писем'
            
    except Mailing.DoesNotExist:
        return False, 'Рассылка не найдена'
    except Exception as e:
        return False, f'Ошибка при отправке: {str(e)}'
