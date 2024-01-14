import re

from django.core.exceptions import ValidationError


FORBIDDEN_USERNAME = 'me'
PATTERN = r'^[\w.@+-]+\Z'


class UsernameValidator:
    def __call__(self, username):
        if username == FORBIDDEN_USERNAME:
            raise ValidationError(
                f'Нельзя использовать "{FORBIDDEN_USERNAME}" '
                'в качестве username'
            )
        if not re.fullmatch(PATTERN, username):
            raise ValidationError(
                f'Username не соответствует паттерну {PATTERN}'
            )
