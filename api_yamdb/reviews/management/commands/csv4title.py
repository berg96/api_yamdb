import csv
from pathlib import Path

from django.core.management import BaseCommand

from reviews.models import Title

BASE_DIR = Path.cwd() / 'static' / 'data'
TEMPLATE_DIR = BASE_DIR / 'titles.csv'


class Command(BaseCommand):
    help = 'Добавление в модель Категории данных из CSV'

    def handle(self, *args, **kwargs):
        # self.stdout.write('Welcome')
        with open(TEMPLATE_DIR) as f:
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                _, created = Title.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category_id=row[3],
                )
