import csv

from django.core.management import BaseCommand

from reviews.models import Category


class Command(BaseCommand):
    help = 'Добавление в модель Категории данных из CSV'

    def handle(self, *args, **kwargs):
        file_path = 'static/data/category.csv'
        with open(file_path, 'r', encoding='utf8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Category.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
