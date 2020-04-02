from django.core.management import BaseCommand

from metarecord.views.export import create_saved_jhs_xml


class Command(BaseCommand):

    help = "Update new version of JHS191 XML to saved file used as a cache."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            action="store_true",
            help="Print output to terminal",
        )

    def handle(self, *args, **options):
        create_saved_jhs_xml(output=options["output"])
