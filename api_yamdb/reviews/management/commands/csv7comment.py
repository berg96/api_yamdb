import csv
from pathlib import Path

from django.core.management import BaseCommand

from reviews.models import Comments

BASE_DIR = Path.cwd() / 'static' / 'data'
TEMPLATE_DIR = BASE_DIR / 'comments.csv'


class Command(BaseCommand):
    help = 'Добавление в модель Категории данных из CSV'

    def handle(self, *args, **kwargs):
        with open(TEMPLATE_DIR) as f:
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                _, created = Comments.objects.get_or_create(
                    id=row[0],
                    text=row[2],
                    pub_date=row[4],
                    author_id=row[3],
                    reviews_id=row[1],
                )
