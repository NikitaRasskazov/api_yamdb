from csv import DictReader

from django.core.management.base import BaseCommand
from yamdb.models import Title, Category, Genre, GenreTitle


class Command(BaseCommand):
    help = "Импортирует данные из csv-файлов"

    def handle(self, *args, **options):
        # Импортирует данные для модели Category
        for row in DictReader(
                open('./static/data/category.csv', 'r', encoding='utf-8')
        ):
            category = Category.objects.get_or_create(
                name=row['name'], slug=row['slug']
            )
            self.stdout.write(f'Category "{category}" создан/обновлен')

        # Импортирует данные для модели Genre
        for row in DictReader(
                open('./static/data/genre.csv', 'r', encoding='utf-8')
        ):
            genre, created = Genre.objects.get_or_create(
                name=row['name'], slug=row['slug']
            )
            self.stdout.write(f'Genre "{genre}" создан/обновлен')

        # Импортирует данные для модели Title
        for row in DictReader(
                open('./static/data/titles.csv', 'r', encoding='utf-8')
        ):
            category = Category.objects.get(slug=row['category'])
            title = Title.objects.create(
                name=row['name'], year=row['year'], category=category
            )
            self.stdout.write(f'Title "{title}" создан/обновлен')

        # Импортирует данные для модели GenreTitle
        for row in DictReader(
                open('./static/data/genre_title.csv', 'r', encoding='utf-8')
        ):
            genre = Genre.objects.get(pk=row['genre_id'])
            title = Title.objects.get(pk=row['title_id'])
            genre_title, created = GenreTitle.objects.get_or_create(
                genre=genre, title=title
            )
            self.stdout.write(f'GenreTitle "{genre_title}" создан/обновлен')
