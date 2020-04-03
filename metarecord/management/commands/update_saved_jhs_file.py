from django.core.management import BaseCommand

from metarecord.views.export import create_saved_jhs_xml


class Command(BaseCommand):

    help = "Update new version of JHS191 XML to saved file used as a cache."

    def handle(self, *args, **options):
        self.stdout.write("Generating XML file...")
        create_saved_jhs_xml()
        self.stdout.write("XML file generated!")
