from django.core.management import BaseCommand

from users.models import User
from yamdb.models import Category, Comment, Genre, GenreTitle, Review, Title


class Command(BaseCommand):
    help = 'Удаляет данные в бд'

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Comment.objects.all().delete()
        Genre.objects.all().delete()
        GenreTitle.objects.all().delete()
        Review.objects.all().delete()
        Title.objects.all().delete()
        User.objects.all().delete()
