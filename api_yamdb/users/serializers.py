from rest_framework import serializers
from . models import User, ROLE_CHOICES
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken


class MaxValueValidator:
    def __init__(self, max_value):
        self.max_value = max_value

    def __call__(self, value):
        if value > self.max_value:
            raise serializers.ValidationError(f'Maximum value is {self.max_value}.')


class UserSignupSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя."""
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            is_active=False
        )
        confirmation_code = default_token_generator.make_token(user)
        subject = 'Подтвердение email-адреса'
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
    role = serializers.ChoiceField(choices=ROLE_CHOICES, default='user')
    last_name = serializers.CharField(validators=[MaxValueValidator(150)])


    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User


class UserTokenSerializer(serializers.Serializer):
    """Сериализатор для подтверждения email-адреса."""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')

        try:
            user = User.objects.get(username=username, is_active=False)
        except User.DoesNotExist:
            raise serializers.ValidationError('Ошибочное имя пользователя или код верификации.')

        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError('Ошибочное имя пользователя или код верификации.')

        user.is_active = True
        user.save()

        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        attrs['token'] = token
        return attrs