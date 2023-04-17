from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserViewSet, UserSignupView, UserTokenView

router = DefaultRouter()
router.register('users', UserViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', UserSignupView.as_view(), name='user_signup'),
    path('v1/auth/token/', UserTokenView.as_view(), name='user_token'),
]
