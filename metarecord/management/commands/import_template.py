from django.core.management.base import BaseCommand
from django.db import transaction

from metarecord.importer.tos import TOSImporter


class Command(BaseCommand):
    help = "Import ERMCS template from Excel file"

    def __init__(self):
        super().__init__()

    def add_arguments(self, parser):
        parser.add_argument("filename", type=str)
        parser.add_argument("sheet_name", type=str)
        parser.add_argument("template_name", type=str, nargs="?", default=None)

    def handle(self, *args, **options):
        filename = options["filename"]
        try:
            tos_importer = TOSImporter(filename)
        except Exception as e:
            print("Cannot open file '%s': %s" % (filename, e))
            return

        with transaction.atomic():
            tos_importer.import_template(
                options["sheet_name"], options["template_name"]
            )
