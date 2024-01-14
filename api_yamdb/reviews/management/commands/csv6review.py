import csv

from django.core.management import BaseCommand

from reviews.models import Review


class Command(BaseCommand):
    help = 'Добавление в модель Review данных из CSV'

    def handle(self, *args, **kwargs):
        file_path = 'static/data/review.csv'
        with open(file_path, 'r', encoding='utf8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Review.objects.get_or_create(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author_id=row['author'],
                    score=row['score'],
                    pub_date=row['pub_date'],
                )
