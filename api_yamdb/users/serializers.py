from rest_framework import serializers
from . models import User, ROLE_CHOICES
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            is_active=False
        )
        confirmation_code = default_token_generator.make_token(user)
        subject = 'Confirm your email address'
        message = f'Please use the following confirmation code to activate your account: {confirmation_code}'
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

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')

        # Find user by username
        try:
            user = User.objects.get(username=username, is_active=False)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid username or confirmation code.')

        # Verify confirmation code
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError('Invalid username or confirmation code.')

        # Activate user account
        user.is_active = True
        user.save()

        # Authenticate user and generate JWT token
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        attrs['token'] = token
        return attrs