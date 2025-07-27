from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mailings.models import Client, Message, Mailing
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Создаёт группы Users и Managers и назначает права менеджерам'

    def handle(self, *args, **options):
        # 1) Группа Users
        users_group, created = Group.objects.get_or_create(name='Users')
        if created:
            self.stdout.write('✔ Группа "Users" создана')

        # 2) Группа Managers
        managers_group, created = Group.objects.get_or_create(name='Managers')
        if created:
            self.stdout.write('✔ Группа "Managers" создана')

        # 3) Менеджеры получают стандартные права view_* и change_* для ключевых моделей
        for model in (Client, Message, Mailing, CustomUser):
            ct = ContentType.objects.get_for_model(model)
            for action in ('view', 'change'):
                codename = f'{action}_{model._meta.model_name}'
                try:
                    perm = Permission.objects.get(content_type=ct, codename=codename)
                    managers_group.permissions.add(perm)
                    self.stdout.write(f'✔ Право "{perm.name}" добавлено для Managers')
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f'⚠ Permission {codename} for {model.__name__} не найдено'
                    ))

        # 4) Добавляем кастомные права для менеджеров
        custom_permissions = [
            # Клиенты
            'view_all_clients',
            # Сообщения
            'view_all_messages',
            # Пользователи
            'block_user',
            # Рассылки
            'view_all_mailings',
            'toggle_mailing',
        ]

        for codename in custom_permissions:
            try:
                perm = Permission.objects.get(codename=codename)
                managers_group.permissions.add(perm)
                self.stdout.write(f'✔ Кастомное право "{perm.name}" добавлено для Managers')
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f'⚠ Кастомное право {codename} не найдено в базе'
                ))

        self.stdout.write(self.style.SUCCESS('✅ Группы Users и Managers успешно настроены'))
