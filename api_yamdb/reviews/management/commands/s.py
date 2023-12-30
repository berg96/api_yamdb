import os
import csv
from pathlib import Path

from django.core.management import BaseCommand

from reviews.models import Category




NAME_OF_PROJECT = 'api_yamdb'
FOLDER_WITH_CSV = ('api_yamdb', 'static', 'data')
NAME_OF_FILES = ['category']



class Command(BaseCommand):
    help = 'Добавление файла '

    def handle(self, *args, **kwargs):
        # self.stdout.write('Welcome')
        print('Создана новая команда manage.py')

        p = Path(__file__)
        try:
            folder_number_in_path = (p.parts.index(NAME_OF_PROJECT))
            standart_path = p.parts[:folder_number_in_path + 1]
            folderCSV = Path(os.path.join(*standart_path, *FOLDER_WITH_CSV))
            print(folderCSV)
        except ValueError:
            print(f'Убедитесь, что вы запускаете файл из проекта {NAME_OF_PROJECT}')
        
        print(folderCSV.is_dir())
        files = folderCSV.glob('*.csv')
        for file in files:
            print(file.name)
            # print(Path(file.name).stem)
            # print(file)
            if Path(file.name).stem in NAME_OF_FILES:
                print(f'Файл {file.name} будет обработан')
                with open(file) as f:
                    if file.name == 'category.csv':
                        reader = csv.reader(f)
                        for row in reader:
                            _, created = Category.objects.get_or_create(
                                # id=row[0],
                                name=row[1],
                                slug=row[2],
                            )
