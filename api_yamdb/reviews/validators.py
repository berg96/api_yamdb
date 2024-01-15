import datetime
import re

from django.core.exceptions import ValidationError


FORBIDDEN_USERNAME = 'me'
PATTERN = r'^[\w.@+-]+\Z'


def correct_year(value):
    current_year = datetime.date.today().year
    if value > current_year:
        raise ValidationError(
            'Введенная дата больше текущего года'
        )


def validate_username(username):
    if username == FORBIDDEN_USERNAME:
        raise ValidationError(
            f'Нельзя использовать "{FORBIDDEN_USERNAME}" '
            'в качестве username'
        )
    if not re.fullmatch(PATTERN, username):
        raise ValidationError(
            f'Username не соответствует паттерну {PATTERN}: {username}'
        )
