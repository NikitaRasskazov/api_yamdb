from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer, UserSignupSerializer, UserTokenSerializer
from .permissions import IsAdmin


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
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    lookup_field = "username"
    search_fields = ('username',) 
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(methods=["GET", "PATCH"], detail=False, permission_classes=[IsAuthenticated])
    def me(self, request):
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
        if pk == 'me':
            user = request.user
        else:
            user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
