from csv import DictReader

from django.core.management.base import BaseCommand

from yamdb.models import Title, Category, Comment, Genre, GenreTitle, Review
from users.models import User


class Command(BaseCommand):
    help = "Импортирует данные из csv-файлов"

    def category_import(self):
        if Category.objects.exists():
            self.stdout.write('Данные уже существуют в Category')
        else:
            for row in DictReader(
                    open('./static/data/category.csv', 'r', encoding='utf-8')
            ):
                category = Category.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
                self.stdout.write(f'Category"{category}" создан')

    def genre_import(self):
        if Genre.objects.exists():
            self.stdout.write('Данные уже существуют в Genre')
        else:
            for row in DictReader(
                    open('./static/data/genre.csv', 'r', encoding='utf-8')
            ):
                genre = Genre.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
                self.stdout.write(f'Genre "{genre}" создан')

    def title_import(self):
        if Title.objects.exists():
            self.stdout.write('Данные уже существуют в Title')
        else:
            for row in DictReader(
                    open('./static/data/titles.csv', 'r', encoding='utf-8')
            ):
                category = Category.objects.get(id=row['category'])
                title = Title.objects.create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=category,
                )
                self.stdout.write(f'Title "{title}" создан')

    def genre_title_import(self):
        if GenreTitle.objects.exists():
            self.stdout.write('Данные уже существуют в GenreTitle')
        else:
            for row in DictReader(
                    open('./static/data/genre_title.csv', 'r', encoding='utf-8')
            ):
                genre_title = GenreTitle.objects.create(
                    id=row['id'],
                    title_id=row['title_id'],
                    genre_id=row['genre_id'],
                )
                self.stdout.write(f'GenreTitle "{genre_title}" создан')

    def user_import(self):
        if User.objects.exists():
            self.stdout.write('Данные уже существуют в User')
        else:
            for row in DictReader(
                    open('./static/data/users.csv', 'r', encoding='utf-8')
            ):
                user = User.objects.create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )
                self.stdout.write(f'User "{user}" создан')

    def review_import(self):
        if Review.objects.exists():
            self.stdout.write('Данные уже существуют в Review')
        else:
            for row in DictReader(
                    open('./static/data/review.csv', 'r', encoding='utf-8')
            ):
                author = User.objects.get(id=row['author'])
                review = Review.objects.create(
                    id=row['id'],
                    author=author,
                    title_id=row['title_id'],
                    pub_date=row['pub_date'],
                    text=row['text'],
                    score=row['score'],
                )
                self.stdout.write(f'Review "{review}" создан')

    def comment_import(self):
        if Comment.objects.exists():
            self.stdout.write('Данные уже существуют в Comment')
        else:
            for row in DictReader(
                    open('./static/data/comments.csv', 'r', encoding='utf-8')
            ):
                author = User.objects.get(id=row['author'])
                comment = Comment.objects.create(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author=author,
                    pub_date=row['pub_date'],
                )
                self.stdout.write(f'Comment "{comment}" создан')

    def handle(self, *args, **kwargs):
        self.user_import()
        self.category_import()
        self.genre_import()
        self.title_import()
        self.genre_title_import()
        self.review_import()
        self.comment_import()
