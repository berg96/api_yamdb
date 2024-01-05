import csv
from pathlib import Path

from django.core.management import BaseCommand

from reviews.models import Review

BASE_DIR = Path.cwd() / 'static' / 'data'
TEMPLATE_DIR = BASE_DIR / 'review.csv'


class Command(BaseCommand):
    help = 'Добавление в модель Категории данных из CSV'
    # id,title_id,text,author,score,pub_date
    def handle(self, *args, **kwargs):
        with open(TEMPLATE_DIR) as f:
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                _, created = Review.objects.get_or_create(
                    id=row[0],
                    title_id=row[1],
                    text=row[2],
                    author_id=row[3],
                    score=row[4],
                    pub_date=row[5],
                )
