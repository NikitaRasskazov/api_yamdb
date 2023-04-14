from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    CommentViewSet,
    ReviewViewSet
)


router_v1 = DefaultRouter()

router_v1.register('categories', CategoryViewSet,)
router_v1.register('genres', GenreViewSet,)
router_v1.register('titles', TitleViewSet,)
router_v1.register('comments', CommentViewSet,)
router_v1.register('review', ReviewViewSet,)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
