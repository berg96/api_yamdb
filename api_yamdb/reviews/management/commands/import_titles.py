import csv
from django.core.management.base import BaseCommand
from reviews.models import Title

class Command(BaseCommand):
    help = 'Import data from CSV file into Model1'

    def handle(self, *args, **options):
        file_path = 'static/data/titles.csv'

        with open(file_path, 'r', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Title.objects.create(
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category']
                )

        self.stdout.write(self.style.SUCCESS(
            f'Successfully imported data for Title from {file_path}'
        ))
