from django.core.management.base import BaseCommand
from django.db import transaction

from metarecord.importer.function import FunctionImporter


class Command(BaseCommand):
    help = "Import function tree from csv file"

    def __init__(self):
        super().__init__()

    def add_arguments(self, parser):
        parser.add_argument("filename", type=str)

    def handle(self, *args, **options):
        filename = options["filename"]
        try:
            function_importer = FunctionImporter(filename)
        except Exception as e:
            print("Cannot open file '%s': %s" % (filename, e))
            return

        with transaction.atomic():
            function_importer.import_functions()
