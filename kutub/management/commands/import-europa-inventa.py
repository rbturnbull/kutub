from django.core.management.base import BaseCommand, CommandError
from kutub import models, readers

class Command(BaseCommand):
    help = 'Imports the Europa Inventa database.'

    def add_arguments(self, parser):
        parser.add_argument('--mss', type=str, default="", help="A CSV dump of manuscripts in the Europa Inventa database.")
        parser.add_argument('--items', type=str, default="", help="A CSV dump of manuscript items in the Europa Inventa database.")
        parser.add_argument('--creators', type=str, default="", help="A CSV dump of creators in the Europa Inventa database.")
        parser.add_argument('--flush', action='store_true', default=False, help="Deletes the database before performing import.")

    def handle(self, *args, **options):
        if options['flush']:
            models.Repository.objects.all().delete()
            models.Manuscript.objects.all().delete()            
            models.ContentItem.objects.all().delete()            

        if options['mss']:
            readers.import_europa_inventa_manuscripts(options['mss'])

        if options['items'] and options['creators']:
            readers.import_europa_inventa_content_items(options['items'], options['creators'])
