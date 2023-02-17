from django.core.management.base import BaseCommand
from django.db import transaction

from metarecord.importer.classification import ClassificationImporter


class Command(BaseCommand):
    help = "Import classification tree from csv file"

    def __init__(self):
        super().__init__()

    def add_arguments(self, parser):
        parser.add_argument("filename", type=str)

    def handle(self, *args, **options):
        filename = options["filename"]
        try:
            classification_importer = ClassificationImporter(filename)
        except Exception as e:
            print("Cannot open file '%s': %s" % (filename, e))
            return

        with transaction.atomic():
            classification_importer.import_classifications()
