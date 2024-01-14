import csv

from django.core.management import BaseCommand

from reviews.models import Genre, Title


class Command(BaseCommand):
    help = 'Добавление в модель Произведений связь с Жанрами из CSV'

    def handle(self, *args, **kwargs):
        file_path = 'static/data/genre_title.csv'
        with open(file_path, 'r', encoding='utf8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])
                title.genre.add(genre)
