from rest_framework import serializers, validators
from rest_framework_simplejwt.tokens import RefreshToken

from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment,
    User,
    ROLE_CHOICES,
    MIN_SCORE,
    MAX_SCORE,
    MAX_LENGTH_USERNAME,
)

MAX_LENGTH_EMAIL = 254


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для управления пользователями."""
    role = serializers.ChoiceField(
        choices=ROLE_CHOICES,
        default='user',
        required=False
    )
    last_name = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME,
        required=False
    )
    username = serializers.RegexField(
        max_length=MAX_LENGTH_USERNAME,
        regex=r'^[\w.@+-]+$',
        error_messages={
            'invalid': 'Это имя пользователя может содержать'
                       'только буквы, цифры и символы @.+-_'
        }
    )

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User
        validators = [
            validators.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username']
            )
        ]


class UserSignupSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя."""
    email = serializers.EmailField(max_length=MAX_LENGTH_EMAIL)
    username = serializers.RegexField(
        max_length=MAX_LENGTH_USERNAME,
        regex=r'^[\w.@+-]+$',
        error_messages={
            'invalid': 'Это имя пользователя может содержать'
                       'только буквы, цифры'
                       'и символы @.+-_'
        }
    )

    def validate(self, data):

        email = data['email']
        username = data['username']
        if (
            User.objects.filter(email=email).exists()
            and not User.objects.filter(username=username).exists()
        ):
            raise serializers.ValidationError(
                'Пользователь с таким email уже зарегистрирован.'
            )

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if email != user.email:
                raise serializers.ValidationError('Указан неверный email.')

        if username != 'me':
            return data
        raise serializers.ValidationError(
            'Имя "me" недоступно для применения.'
        )

    def create(self, validated_data):
        try:
            user = User.objects.get(
                Q(email=validated_data['email'])
                | Q(username=validated_data['username'])
            )
        except ObjectDoesNotExist:
            user = User.objects.create(
                email=validated_data['email'],
                username=validated_data['username'],
                is_active=False
            )
        confirmation_code = default_token_generator.make_token(user)
        subject = 'Подтверждение email-адреса'
        message = (f'Пожалуйста, используйте этот код подтверждения для '
                   f'активации вашей учетной записи: {confirmation_code}')
        send_mail(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=[validated_data['email']],
            fail_silently=False,
        )
        return user


class UserTokenSerializer(serializers.Serializer):
    """Сериализатор для подтверждения email-адреса."""
    username = serializers.CharField(max_length=MAX_LENGTH_USERNAME)
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')

        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError(
                'Ошибочное имя пользователя или код верификации.'
            )

        user.is_active = True
        user.save()

        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        attrs['token'] = token
        return attrs


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id', )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id', )


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    score = serializers.IntegerField(
        validators=(
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE)
        ))

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title', 'author')

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            author = request.user
            title_id = self.context.get('view').kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    'Больше одного отзыва отзыва написать нельзя'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
