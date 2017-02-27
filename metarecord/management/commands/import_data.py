from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from metarecord.importer.tos import TOSImporter, TOSImporterException


class Command(BaseCommand):
    help = "Import ERMCS data from Excel file"

    def __init__(self):
        super().__init__()

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        filename = options['filename']
        try:
            tos_importer = TOSImporter(filename)
        except Exception as e:
            self.stderr.write(self.style.ERROR("Cannot open file '%s': %s" % (filename, e)))
            return

        try:
            with transaction.atomic():
                tos_importer.import_data()
        except TOSImporterException as e:
            self.stderr.write(self.style.ERROR(e))
