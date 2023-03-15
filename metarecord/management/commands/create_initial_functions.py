from django.core.management.base import BaseCommand

from metarecord.models import Classification, Function


class Command(BaseCommand):
    help = "Create initial functions (for backwards compatibility)."

    def __init__(self):
        super().__init__()

    def handle(self, *args, **options):
        print("Creating initial functions...")

        for classification in Classification.objects.all():
            obj, created = Function.objects.get_or_create(classification=classification)
            if created:
                print(classification)

        print("Done.")
