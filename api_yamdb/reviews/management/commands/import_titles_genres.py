import csv
from django.core.management.base import BaseCommand
from reviews.models import Genre, Title

class Command(BaseCommand):
    help = 'Import data from CSV file into Model1'

    def handle(self, *args, **options):
        file_path = 'static/data/genre_title.csv'

        with open(file_path, 'r', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = Title.objects.get(pk=row['title_id'])
                genre = Genre.objects.get(pk=row['genre_id'])
                title.genre.add(genre)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully imported data for Title_Genre from {file_path}'
        ))
