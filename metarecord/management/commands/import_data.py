from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from metarecord.importer.tos import TOSImporter, TOSImporterException


class Command(BaseCommand):
    help = "Import ERMCS data from Excel file"

    def __init__(self):
        super().__init__()

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)
        parser.add_argument('--ignore-errors', action='store_true')

    def handle(self, *args, **options):
        filename = options['filename']
        try:
            tos_importer = TOSImporter(options)
            tos_importer.open(filename)
        except Exception as e:
            raise CommandError("Cannot open file '%s': %s" % (filename, e))

        try:
            with transaction.atomic():
                tos_importer.import_data()
        except TOSImporterException as e:
            raise CommandError(e)
