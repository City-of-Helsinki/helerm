import logging
import re

from django.conf import settings
from django.db.models import QuerySet
from lxml import etree, objectify

from metarecord.models import Classification

from .builder import build_tos_document

logger = logging.getLogger(__name__)


class JHSExporterException(Exception):
    pass


def fix_xml_declaration_single_quotes(xml: bytes) -> bytes:
    """
    Fix XML declaration single quotes to double quotes.

    This is a hard-coded feature in lxml, which, at the time of writing,
    isn't getting fixed anytime soon. This is a workaround for that.
    """

    def _replace_single_quotes_with_double_quotes(m: re.Match):
        attrs = m.group(2)
        return m.group(1) + attrs.replace(b"'", b'"') + m.group(3)

    return re.sub(
        rb"^(<\?xml)(.+)(\?>)", _replace_single_quotes_with_double_quotes, xml
    )


class JHSExporter:
    @staticmethod
    def get_queryset():
        # at least for now include all classifications
        return Classification.objects.all()

    def create_xml(self, queryset: QuerySet[Classification] = None):
        queryset = queryset or self.get_queryset()
        try:
            tos_root = build_tos_document(queryset)
        except Exception as e:
            logger.error("ERROR building XML: %s" % e)
            raise JHSExporterException(e) from e

        xml = etree.tostring(
            tos_root,
            xml_declaration=True,
            encoding="utf-8",
            pretty_print=True,
        )
        xml = fix_xml_declaration_single_quotes(xml)

        if settings.XML_EXPORT_VALIDATION_ENABLED:
            self.validate_xml(xml)

        return xml

    @staticmethod
    def validate_xml(xml: bytes):
        logger.info("Validating XML...")

        with open(settings.JHS_XSD_PATH, "r") as f:
            schema = etree.XMLSchema(file=f)
        parser = objectify.makeparser(schema=schema)

        try:
            objectify.fromstring(xml, parser)
        except Exception as e:
            logger.error("ERROR validating XML: %s" % e)
            raise JHSExporterException(e) from e

    def export_data(self, filename):
        logger.info("Exporting data...")
        xml = self.create_xml()

        try:
            with open(filename, "wb") as f:
                logger.info("Writing to the file...")
                f.write(xml)
                logger.info("File written")
        except Exception as e:
            logger.error("ERROR writing to the file: %s" % e)
            raise JHSExporterException(e) from e
