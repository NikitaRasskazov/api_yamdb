from datetime import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

LEN_STR_TEXT = 20
MAX_LENGTH_REVIEW = 200


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
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
        max_length=2000,
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
        return self.name


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
        max_length=200
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    def __str__(self):
        return self.text[:LEN_STR_TEXT]
