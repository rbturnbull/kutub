from django.core.management.base import BaseCommand, CommandError
from kutub import models, readers

class Command(BaseCommand):
    help = 'Imports the Europa Inventa database.'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, default="", help="An Excel file with the listing of the Bischoff mss.")
        parser.add_argument('omeka_xml', type=str, default="", help="An Omeka XML file of the collection.")

    def handle(self, *args, **options):
        readers.import_bischoff(options['excel_file'], options['omeka_xml'])
