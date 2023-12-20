import csv
from django.core.management.base import BaseCommand
from reviews.models import Category

class Command(BaseCommand):
    help = 'Import data from CSV file into Model1'

    def handle(self, *args, **options):
        file_path = 'static/data/category.csv'

        with open(file_path, 'r', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Category.objects.create(**row)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully imported data for Category from {file_path}'
        ))
