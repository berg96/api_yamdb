import csv

from django.core.management import BaseCommand

from reviews.models import Comments


class Command(BaseCommand):
    help = 'Добавление в модель Комментария данных из CSV'

    def handle(self, *args, **kwargs):
        file_path = 'static/data/comments.csv'
        with open(file_path, 'r', encoding='utf8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                _, created = Comments.objects.get_or_create(
                    id=row['id'],
                    text=row['text'],
                    pub_date=row['pub_date'],
                    author_id=row['author'],
                    review_id=row['review_id'],
                )
