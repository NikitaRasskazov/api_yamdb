from datetime import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser

from validators import validate_username

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
        verbose_name='Биография',
        blank=True
    )
    username = models.CharField(
        verbose_name='Логин',
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
        validators=[validate_username]
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=MAX_LENGTH_ROLE,
        choices=ROLE_CHOICES,
        default='user',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_superuser or self.role == "admin"

    @property
    def is_moder(self):
        return self.role == 'moderator'


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name="Название категории",
    )
    slug = models.SlugField(
        unique=True,
        max_length=MAX_LENGTH_SLUG,
        verbose_name="Идентификатор категории",
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:LEN_STR_TEXT]


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name="Название жанра",
    )
    slug = models.SlugField(
        unique=True,
        max_length=MAX_LENGTH_SLUG,
        verbose_name="Идентификатор жанра",
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:LEN_STR_TEXT]


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name="Название произведения",
    )
    year = models.IntegerField(
        validators=[
            MinValueValidator(1, message='Год должен быть натуральным числом'),
            MaxValueValidator(
                datetime.now().year,
                message='Год не может быть больше текущего'
            )
        ],
        verbose_name="Год выпуска",
    )
    description = models.CharField(
        max_length=MAX_LENGTH_DESCRIPTION,
        null=True,
        blank=True,
        verbose_name="Описание произведения",
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Категории произведения",
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name="Жанры произведения",
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:LEN_STR_TEXT]


class GenreTitle(models.Model):
    """Промежуточная модель GenreTitle."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name="Жанр",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="Произведение",
    )

    class Meta:
        verbose_name = 'Жанр и произведение'
        verbose_name_plural = 'Жанры и произведения'


class Review(models.Model):
    """Модель отзывов."""
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
        error_messages={'validators':
                        f'Поставьте оценку от {MIN_SCORE} до {MAX_SCORE}!'
                        }
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique review'
            )]

    def __str__(self):
        return self.text[:LEN_STR_TEXT]


class Comment(models.Model):
    """Модель комментриев."""
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

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:LEN_STR_TEXT]
