from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from mailings.models import Mailing, MailingAttempt


class Command(BaseCommand):
    """Команда для запуска активных рассылок вручную"""

    help = 'Запуск активных рассылок вручную'

    def handle(self, *args, **options):
        now = timezone.now()
        mailings = Mailing.objects.filter(
            status__in=['created', 'started'],  # Исправлен синтаксис фильтра
            start_time__lte=now,
            end_time__gte=now,
            owner__is_active=True
        )

        for mailing in mailings:
            try:
                # Обновляем статус на 'started'
                mailing.status = 'started'
                mailing.save(update_fields=['status'])

                clients = mailing.clients.all()
                if not clients.exists():
                    self.stdout.write(self.style.WARNING(
                        f'У рассылки {mailing.id} нет получателей'
                    ))
                    continue

                success_count = 0
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
                        self.stdout.write(self.style.ERROR(
                            f'Ошибка отправки клиенту {client.email}: {str(e)}'
                        ))

                    # Создаем запись о попытке
                    MailingAttempt.objects.create(
                        mailing=mailing,
                        status=status,
                        server_response=server_response
                    )

                # Обновляем статус рассылки
                mailing.status = 'completed' if success_count > 0 else 'failed'
                mailing.save(update_fields=['status'])

                self.stdout.write(self.style.SUCCESS(
                    f'Рассылка {mailing.id} завершена. Успешно отправлено: {success_count}/{clients.count()}'
                ))

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'Ошибка при обработке рассылки {mailing.id}: {str(e)}'
                ))
                # Пробуем сохранить ошибку в статус
                try:
                    mailing.status = 'failed'
                    mailing.save(update_fields=['status'])
                except:
                    pass
