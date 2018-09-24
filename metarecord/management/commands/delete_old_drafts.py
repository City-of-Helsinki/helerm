from django.core.management.base import BaseCommand
from django.db import transaction

from metarecord.models.function import Function


class Command(BaseCommand):
    help = 'Delete non approved functions that are older than latest approved version.'

    def handle(self, *args, **options):
        approved_functions = Function.objects.latest_approved()

        with transaction.atomic():
            for function in approved_functions:
                function.delete_old_non_approved_versions()

        print('Successfully deleted old non approved functions!')
