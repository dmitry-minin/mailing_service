from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets
from django.utils import timezone
from django.conf import settings


class CustomUser(AbstractUser):
    """
    Custom user model.
    """
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")

    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватар")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Телефон")
    country = models.CharField(max_length=100, null=True, blank=True, verbose_name="Страна")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class EmailActivation(models.Model):
    """
    Токены для активации по email.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created + timezone.timedelta(days=1)

    @classmethod
    def create_token(cls, user):
        token = secrets.token_urlsafe(16)
        return cls.objects.create(user=user, token=token)
