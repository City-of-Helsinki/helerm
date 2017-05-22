import logging
from django.http import HttpResponse
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from metarecord.exporter.jhs import JHSExporter, JHSExporterException

logger = logging.getLogger(__name__)


class ExportView(APIView):
    def get(self, request, format=None):
        exporter = JHSExporter(output=True)

        try:
            xml = exporter.create_xml()
        except JHSExporterException as e:
            logger.error('Exception while creating a XML export: %s' % e)
            raise APIException('Could not create an XML export.')

        response = HttpResponse(xml, content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename="helerm-export.xml"'

        return response
