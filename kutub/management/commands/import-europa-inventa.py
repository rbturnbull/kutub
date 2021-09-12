from django.core.management.base import BaseCommand, CommandError
from kutub.readers import import_europa_inventa

class Command(BaseCommand):
    help = 'Imports the Europa Inventa database.'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str, help="A CSV dump of the Europa Inventa database.")

    def handle(self, *args, **options):
        import_europa_inventa(options['csv'])

