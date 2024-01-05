import csv
from pathlib import Path

from django.core.management import BaseCommand

from api.models import MyUser

BASE_DIR = Path.cwd() / 'static' / 'data'
TEMPLATE_DIR = BASE_DIR / 'users.csv'


class Command(BaseCommand):
    help = 'Добавление в модель Категории данных из CSV'

    def handle(self, *args, **kwargs):
        # self.stdout.write('Welcome')
        with open(TEMPLATE_DIR) as f:
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                _, created = MyUser.objects.get_or_create(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6],
                )
