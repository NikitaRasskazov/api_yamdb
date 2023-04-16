from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer, UserSignupSerializer, UserTokenSerializer


class UserSignupView(APIView):
    serializer_class = UserSignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserTokenView(APIView):
    serializer_class = UserTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'token': serializer.validated_data['token']})


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_serializer_class(self):
        if self.action == 'me':
            return UserSerializer
        return super().get_serializer_class()

    @action(methods=['get', 'patch'], detail=True)
    def me(self, request):
        serializer = self.get_serializer_class()
        user = get_object_or_404(User, username=request.user.username)
        if self.request.method == 'PATCH':
            serializer = serializer(user, request.data, partial=True)
            if serializer.is_valid():
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