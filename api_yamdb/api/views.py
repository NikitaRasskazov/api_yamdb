from django_filters.rest_framework import (
    DjangoFilterBackend, FilterSet, CharFilter, NumberFilter
)
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
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
from .mixins import CustomViewSet


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleFilterSet(FilterSet):
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')
    name = CharFilter()
    year = NumberFilter()

    class Meta:
        model = Title
        fields = []


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
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
        serializer.save(author=self.request.user, review=self.get_review())
