from django.core.management import BaseCommand, call_command

COMMANDS = [
    'csv1user',
    'csv2genre',
    'csv3category',
    'csv4title',
    'csv5genretitle',
    'csv6review',
    'csv7comment',
]


class Command(BaseCommand):
    help = 'Импорт всех файлов csv'

    def handle(self, *args, **kwargs):
        for command in COMMANDS:
            call_command(command)
