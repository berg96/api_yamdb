import csv

from django.core.management import BaseCommand

from reviews.models import Title


class Command(BaseCommand):
    help = 'Добавление в модель Произведений данных из CSV'

    def handle(self, *args, **kwargs):
        file_path = 'static/data/titles.csv'
        with open(file_path, 'r', encoding='utf8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Title.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category'],
                )
