from rest_framework import viewsets

from yamdb.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer, TitleCreateSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = ()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = ()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = ()
    filterset_fields = ['category__slug', 'genre__slug', 'name', 'year']

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return TitleCreateSerializer
        return TitleSerializer
