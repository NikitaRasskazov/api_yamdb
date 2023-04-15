from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    ]


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True
    )
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        'Email',
        unique=True,
    )
    role = models.CharField(
        'Роль',
        max_length=15,
        choices=ROLE_CHOICES,
        default='user',
    )

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['username', 'email'],
    #             name='unique_user')
    #     ]


