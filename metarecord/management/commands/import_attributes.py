from django.core.management.base import BaseCommand
from django.db import transaction

from metarecord.importer.tos import TOSImporter


class Command(BaseCommand):
    help = "Import attributes from Excel file"

    def __init__(self):
        super().__init__()

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        filename = options['filename']
        try:
            tos_importer = TOSImporter(options)
            tos_importer.open(filename)
        except Exception as e:
            print("Cannot open file '%s': %s" % (filename, e))
            return

        with transaction.atomic():
            tos_importer.import_attributes()
