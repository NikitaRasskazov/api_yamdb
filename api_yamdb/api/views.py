from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from yamdb.models import Category, Genre, Title, Review
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleCreateSerializer,
    CommentSerializer,
    ReviewSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = ()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = ()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    serializer_class = TitleSerializer
    permission_classes = ()
    filterset_fields = ['category__slug', 'genre__slug', 'name', 'year']

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return TitleCreateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = ()

    def get_title(self):
        return get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = ()

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_review())
