from datetime import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser

LEN_STR_TEXT = 20
MAX_LENGTH_TEXT = 200
MAX_LENGTH_NAME = 256
MAX_LENGTH_SLUG = 50
MAX_LENGTH_USERNAME = 150
MAX_LENGTH_DESCRIPTION = 2000
MAX_LENGTH_ROLE = 15
MIN_SCORE = 1
MAX_SCORE = 10

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
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
    )
    email = models.EmailField(
        'Email',
        unique=True,
    )
    role = models.CharField(
        'Роль',
        max_length=MAX_LENGTH_ROLE,
        choices=ROLE_CHOICES,
        default='user',
    )

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_superuser or self.role == "admin"

    @property
    def is_moder(self):
        return self.role == 'moderator'


class Category(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_NAME)
    slug = models.SlugField(unique=True, max_length=MAX_LENGTH_SLUG)

    def __str__(self):
        return self.name[:LEN_STR_TEXT]


class Genre(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_NAME)
    slug = models.SlugField(unique=True, max_length=MAX_LENGTH_SLUG)

    def __str__(self):
        return self.name[:LEN_STR_TEXT]


class Title(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_NAME)
    year = models.IntegerField(
        validators=[
            MinValueValidator(1, message='Год должен быть натуральным числом'),
            MaxValueValidator(
                datetime.now().year,
                message='Год не может быть больше текущего'
            )
        ],
    )
    description = models.CharField(
        max_length=MAX_LENGTH_DESCRIPTION,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
    )

    def __str__(self):
        return self.name[:LEN_STR_TEXT]


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    text = models.CharField(
        max_length=MAX_LENGTH_TEXT
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        'оценка',
        validators=(
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE)
        ),
        error_messages={'validators': 'Поставьте оценку от 1 до 10!'}
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique review'
            )]

    def __str__(self):
        return self.text[:LEN_STR_TEXT]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    text = models.CharField(
        max_length=MAX_LENGTH_TEXT
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        return self.text[:LEN_STR_TEXT]
