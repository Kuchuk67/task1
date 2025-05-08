from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    nick_telegram = models.CharField(
        max_length=50,
        default=None,
        null=True,
        blank=True,
        verbose_name="Telegram ник пользователя",
        help_text="Telegram ник для бота рассылки",
    )
    chat_id_telegram = models.CharField(
        max_length=50,
        default=None,
        null=True,
        blank=True,
        verbose_name="Telegram chat_id пользователя",
        help_text="Telegram chat_id для бота рассылки",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def __repr__(self):
        return f"{self.pk} {self.email}"
