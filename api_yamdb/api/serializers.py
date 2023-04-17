from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from yamdb.models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id', )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id', )


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    score = serializers.IntegerField(
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ))

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title', 'author')

    def validate_unique_review(self, data):
        request = self.context['request']
        if request.method == 'POST':
            author = request.user
            title_id = self.context.get('view').kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    'Больше одного отзыва отзыва написать нельзя'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
