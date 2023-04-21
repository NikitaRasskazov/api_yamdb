from rest_framework import mixins, viewsets, filters
from rest_framework.pagination import PageNumberPagination

from .permissions import IsAdminOrReadOnly


class CustomViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly, )

    def get_queryset(self):
        return self.queryset.all()
