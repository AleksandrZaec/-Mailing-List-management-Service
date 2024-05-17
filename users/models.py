from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}
ACTIVE_CHOICES = [
    (True, 'Активен'),
    (False, 'Неактивен'),
]


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    phone = models.CharField(max_length=20, verbose_name='Телефон', **NULLABLE)
    verification_token = models.CharField(max_length=100, blank=True, verbose_name='Код подтверждения почты')
    is_active = models.BooleanField(default=False, choices=ACTIVE_CHOICES, verbose_name='Почта активирована')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

