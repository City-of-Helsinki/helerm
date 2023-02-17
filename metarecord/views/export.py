import logging
import os

from django.conf import settings
from django.http import HttpResponse
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from metarecord.exporter.jhs import JHSExporter, JHSExporterException
from metarecord.models import Function
from metarecord.views.function import FunctionFilterSet

logger = logging.getLogger(__name__)


def create_saved_jhs_xml():
    try:
        exporter = JHSExporter()
        xml = exporter.create_xml()
        save_jhs_export_to_file(xml)

        return xml

    except JHSExporterException as e:
        logger.error("Exception while creating a cached JHS191 XML export: %s" % e)
        raise APIException("Could not create an XML export.")


def save_jhs_export_to_file(xml):
    directory = os.path.join(settings.MEDIA_ROOT, "export")

    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, "helerm-jhs191-export.xml")

    with open(file_path, "wb") as f:
        f.write(xml)

    return file_path


class ExportView(APIView):
    def get(self, request, format=None):
        exporter = JHSExporter()
        queryset = exporter.get_queryset()

        queryset = FunctionFilterSet(
            request.query_params, queryset=queryset, request=request
        ).qs

        state = self.request.query_params.get("state")
        if state in [i[0] for i in Function.STATE_CHOICES]:
            queryset = queryset.filter(state=state)

        try:
            xml = exporter.create_xml(queryset=queryset)
        except JHSExporterException as e:
            logger.error("Exception while creating a XML export: %s" % e)
            raise APIException("Could not create an XML export.")

        response = HttpResponse(xml, content_type="application/xml")
        response["Content-Disposition"] = 'attachment; filename="helerm-export.xml"'

        return response


class JHSExportViewSet(ViewSet):
    def list(self, request, format=None):
        export_file_path = os.path.join(
            settings.MEDIA_ROOT + "/export/helerm-jhs191-export.xml"
        )

        try:
            xml = open(export_file_path)
        except FileNotFoundError:
            xml = None

        if not xml:
            xml = create_saved_jhs_xml()

        response = HttpResponse(xml, content_type="application/xml")
        response[
            "Content-Disposition"
        ] = 'attachment; filename="helerm-jhs191-export.xml"'

        return response
