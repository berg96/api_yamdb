import datetime

from django.core.exceptions import ValidationError


def correct_year(value):
    current_year = datetime.date.today().year
    if value > current_year:
        raise ValidationError(
            'Введенная дата больше текущего года'
        )
