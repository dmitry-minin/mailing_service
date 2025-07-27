from django.db import models
from django.conf import settings


class Client(models.Model):
    """Модель получателя рассылки (клиента)"""
    email = models.EmailField(unique=True, verbose_name="Email получателя")
    full_name = models.CharField(max_length=255, verbose_name="ФИО получателя")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="clients"
    )

    def __str__(self):
        return f"{self.full_name} <{self.email}>"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        permissions = [
            ("view_all_clients", "Может просматривать всех клиентов"),
        ]


class Message(models.Model):
    """Модель сообщения для рассылки"""
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Текст письма")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="messages",
        null=True
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        permissions = [
            ("view_all_messages", "Может просматривать все сообщения"),
        ]


class Mailing(models.Model):
    """Модель рассылки"""
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_time = models.DateTimeField(verbose_name="Дата и время начала")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='created',
        verbose_name="Статус рассылки"
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name="Сообщение",
        related_name="mailings"
    )
    clients = models.ManyToManyField(Client, related_name="mailings", verbose_name="Получатели")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="mailings"
    )

    def __str__(self):
        return f"Рассылка #{self.id} ({self.status})"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("view_all_mailings", "Может просматривать все рассылки"),
            ("toggle_mailing", "Может включать/отключать рассылки"),
        ]


class MailingAttempt(models.Model):
    """Модель попытки отправки рассылки"""
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('fail', 'Не успешно'),
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name="attempts")
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Время попытки")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="Статус")
    server_response = models.TextField(verbose_name="Ответ почтового сервера")

    def __str__(self):
        return f"Попытка для рассылки #{self.mailing.id} — {self.status}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
