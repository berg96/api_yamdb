import csv

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Добавление в модель Пользователей данных из CSV'

    def handle(self, *args, **kwargs):
        file_path = 'static/data/users.csv'
        with open(file_path, 'r', encoding='utf8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                User.objects.get_or_create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )
