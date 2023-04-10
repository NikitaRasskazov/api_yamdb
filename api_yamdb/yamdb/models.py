from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.DateTimeField()  # во views -> year.year или сделать через IntegerField
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL(),
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name
