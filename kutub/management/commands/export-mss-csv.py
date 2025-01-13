from django.core.management.base import BaseCommand, CommandError
from kutub import export, models

class Command(BaseCommand):
    help = 'Exports the manuscripts to a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str, default="", help="A filepath to export to.")

    def handle(self, *args, **options):
        with open(options['csv'], "w") as f:
            export.all_manuscripts_to_csv(f)
