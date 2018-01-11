import logging

from django.http import HttpResponse
from rest_framework.exceptions import APIException
from rest_framework.views import APIView

from metarecord.exporter.jhs import JHSExporter, JHSExporterException
from metarecord.models import Function
from metarecord.views.function import FunctionFilterSet

logger = logging.getLogger(__name__)


class ExportView(APIView):
    def get(self, request, format=None):
        exporter = JHSExporter(output=True)
        queryset = exporter.get_queryset()

        queryset = FunctionFilterSet(request.query_params, queryset=queryset, request=request).qs

        state = self.request.query_params.get('state')
        if state in [i[0] for i in Function.STATE_CHOICES]:
            queryset = queryset.filter(state=state)

        try:
            xml = exporter.create_xml(queryset=queryset)
        except JHSExporterException as e:
            logger.error('Exception while creating a XML export: %s' % e)
            raise APIException('Could not create an XML export.')

        response = HttpResponse(xml, content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename="helerm-export.xml"'

        return response
