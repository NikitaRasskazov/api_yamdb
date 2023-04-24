from django.db.models import Avg
from django_filters.rest_framework import (
    CharFilter,
    DjangoFilterBackend,
    FilterSet,
    NumberFilter,
)
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import Category, Genre, Review, Title, User
from .permissions import IsAdmin, IsAdminOrModerOrAuthor, IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateSerializer,
    TitleSerializer,
    UserSerializer,
    UserSignupSerializer,
    UserTokenSerializer,
)
from .mixins import CustomViewSet


class UserSignupView(APIView):
    """Вьюсет для регистрации пользователя."""

    serializer_class = UserSignupSerializer

    def post(self, request):
        """Регистрация пользователя."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserTokenView(APIView):
    """Вьюсет для получения токена авторизации."""

    serializer_class = UserTokenSerializer

    def post(self, request):
        """Создание токена для авторизации пользователя."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'token': serializer.validated_data['token']})


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для управления пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    lookup_field = "username"
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        """Возврат или редактирование данных пользователя."""
        serializer = self.get_serializer_class()
        user = get_object_or_404(User, username=request.user.username)
        if self.request.method == 'PATCH':
            serializer = serializer(user, request.data, partial=True)
            if serializer.is_valid():
                serializer.validated_data['role'] = request.user.role
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):
        """Удаление пользователя."""
        if pk == 'me':
            user = request.user
        else:
            user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(CustomViewSet):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CustomViewSet):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleFilterSet(FilterSet):
    """Фильтрация для произведений."""

    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')
    name = CharFilter()
    year = NumberFilter()

    class Meta:
        model = Title
        fields = []


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet
    permission_classes = (IsAdminOrReadOnly, )

    def get_serializer_class(self):
        """Определяет сериализатор для произведений."""
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrModerOrAuthor,)
    pagination_class = PageNumberPagination

    def get_title(self):
        """Получение произведений."""
        return get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        """Переопределяем метод get_queryset."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Создание новый записи в базе данных."""
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментриев."""

    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrModerOrAuthor,)

    def get_review(self):
        """Получение отзывов."""
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        """Переопределяем метод get_queryset."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Создание новый записи в базе данных."""
        serializer.save(author=self.request.user, review=self.get_review())
