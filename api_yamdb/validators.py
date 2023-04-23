from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_username(value):
    """Валидация имени пользователя."""
    if not value:
        raise ValidationError(
            'Это поле обязательно для заполнения.'
        )

    regex_validator = RegexValidator(
        regex=r'^[\w.@+-]+$',
        message=(
            'Это имя пользователя может содержать '
            'только буквы, цифры и символы @.+-_'
        )
    )
    regex_validator(value)
