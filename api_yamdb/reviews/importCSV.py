import os
import csv
from pathlib import Path
import fnmatch

# from api_yamdb.api_yamdb.api.models import Category

from reviews.models import Category


from inspect import getsourcefile
from os.path import abspath
import re


NAME_OF_PROJECT = 'api_yamdb'
FOLDER_WITH_CSV = ('api_yamdb', 'static', 'data')


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
    with open(file) as f:
        if file.name == 'category.csv':
            reader = csv.reader(f)
            for row in reader:
                _, created = Category.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )
                # creates a tuple of the new object or
                # current object and a boolean of if it was created

# тот пример, который я взял за основу
# https://stackoverflow.com/questions/2459979/how-to-import-csv-data-into-django-models



# можно настроить вообще через админку
# https://fixmypc.ru/post/vypolniaem-import-csv-v-django-ispolzuia-admin-panel/
                
# МОжно через форму
# https://studygyaan.com/django/import-data-from-csv-sheets-into-databases-using-django
