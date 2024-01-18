import datetime
import re

from django.conf import settings
from django.core.exceptions import ValidationError

PATTERN = r'^[\w.@+-]+\Z'


def validate_year(year):
    current_year = datetime.date.today().year
    if year > current_year:
        raise ValidationError(
            f'Введенная дата больше текущего года: {year} > {current_year}'
        )
    return year


def validate_username(username):
    if username == settings.SELF_PROFILE_NAME:
        raise ValidationError(
            f'Нельзя использовать "{settings.SELF_PROFILE_NAME}" '
            'в качестве username'
        )
    if not re.fullmatch(PATTERN, username):
        invalid_chars = ", ".join(
            char for char in username if not re.match(PATTERN, char)
        )
        raise ValidationError(
            f'Символы в username, не соответствующие паттерну: {invalid_chars}'
        )
    return username
