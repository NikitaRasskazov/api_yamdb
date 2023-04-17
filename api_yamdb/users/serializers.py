from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from . models import User, ROLE_CHOICES
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404


class UserSignupSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя."""
    email = serializers.EmailField(max_length=254)
    username = serializers.RegexField(
        max_length=150,
        regex=r'^[\w.@+-]+$',
        error_messages={
            'invalid': 'Это имя пользователя может содержать только буквы, цифры'
                       'и символы @.+-_'
        }
    )

    def validate(self, data):

        email = data['email']
        username = data['username']
        if User.objects.filter(email=email).exists() and not User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Пользователь с таким email уже зарегистрирован.')

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if email != user.email:
                raise serializers.ValidationError('Указан неверный email.')

        if username != 'me':
            return data
        raise serializers.ValidationError('Имя "me" недоступно для применения.')
    
    def create(self, validated_data):
        try:
            user = User.objects.get(Q(email=validated_data['email']) | Q(username=validated_data['username']))
            
            confirmation_code = default_token_generator.make_token(user)
            subject = 'Подтверждение email-адреса'
            message = f'Пожалуйста, используйте следующий код подтверждения для активации вашей учетной записи: {confirmation_code}'
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[validated_data['email']],
                fail_silently=False,
            )
            
            return user


        except ObjectDoesNotExist:
            user = User.objects.create(
                email=validated_data['email'],
                username=validated_data['username'],
                is_active=False
            )
            confirmation_code = default_token_generator.make_token(user)
            subject = 'Подтверждение email-адреса'
            message = f'Пожалуйста, используйте следующий код подтверждения для активации вашей учетной записи: {confirmation_code}'
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[validated_data['email']],
                fail_silently=False,
            )
            return user


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""
    role = serializers.ChoiceField(choices=ROLE_CHOICES, default='user', required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    username = serializers.RegexField(
        max_length=150,
        regex=r'^[\w.@+-]+$',
        error_messages={
            'invalid': 'Это имя пользователя может содержать только буквы, цифры'
                       'и символы @.+-_'
        }
    )

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username']
            )
        ]


class UserTokenSerializer(serializers.Serializer):
    """Сериализатор для подтверждения email-адреса."""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')

        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError('Ошибочное имя пользователя или код верификации.')

        user.is_active = True
        user.save()

        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        attrs['token'] = token
        return attrs