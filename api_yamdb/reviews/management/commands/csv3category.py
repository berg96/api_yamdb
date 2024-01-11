import csv
from pathlib import Path

from django.core.management import BaseCommand

from reviews.models import Category

BASE_DIR = Path.cwd() / 'static' / 'data'
TEMPLATE_DIR = BASE_DIR / 'category.csv'


class Command(BaseCommand):
    help = 'Добавление в модель Категории данных из CSV'

    def handle(self, *args, **kwargs):
        # self.stdout.write('Welcome')
        with open(TEMPLATE_DIR) as f:
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                _, created = Category.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )
