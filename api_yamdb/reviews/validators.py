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
    invalid_chars = re.sub(PATTERN, '', username)
    if invalid_chars:
        raise ValidationError(
            'Недопустимые символы в username: '
            f'{"".join(set(invalid_chars))}'
        )
    return username
