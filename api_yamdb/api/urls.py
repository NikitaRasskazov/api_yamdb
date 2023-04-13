from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet


router = DefaultRouter()

router.register('categories', CategoryViewSet,)
router.register('genres', GenreViewSet,)
router.register('titles', TitleViewSet,)
router.register('reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('v1/', include(router.urls)),
]
