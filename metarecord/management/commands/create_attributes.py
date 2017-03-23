from django.core.management.base import BaseCommand

from metarecord.models.attribute import create_predefined_attributes


class Command(BaseCommand):
    help = "Create predefined attributes."

    def __init__(self):
        super().__init__()

    def handle(self, *args, **options):
        create_predefined_attributes()
