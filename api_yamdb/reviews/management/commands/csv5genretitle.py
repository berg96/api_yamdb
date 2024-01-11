import csv
from pathlib import Path

from django.core.management import BaseCommand

from reviews.models import Genre, Title

BASE_DIR = Path.cwd() / 'static' / 'data'
TEMPLATE_DIR = BASE_DIR / 'genre_title.csv'


class Command(BaseCommand):
    help = 'Добавление в модель Категории данных из CSV'

    def handle(self, *args, **kwargs):
        # self.stdout.write('Welcome')
        with open(TEMPLATE_DIR) as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])
                title.genre.add(genre)
