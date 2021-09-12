from django.core.management.base import BaseCommand, CommandError
from kutub.readers import import_europa_inventa
from kutub import models, readers

class Command(BaseCommand):
    help = 'Imports the Europa Inventa database.'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str, help="A CSV dump of the Europa Inventa database.")
        parser.add_argument('--flush', action='store_true', default=False, help="Deletes the database before performing import.")

    def handle(self, *args, **options):
        if options['flush']:
            models.Repository.objects.all().delete()
            models.Manuscript.objects.all().delete()            

        readers.import_europa_inventa(options['csv'])

