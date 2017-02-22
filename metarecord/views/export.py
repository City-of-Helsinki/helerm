from django.http import HttpResponse
from rest_framework.views import APIView
from metarecord.exporter.jhs import JHSExporter


class ExportView(APIView):
    def get(self, request, format=None):
        exporter = JHSExporter(output=True)
        xml = exporter.create_xml()
        response = HttpResponse(xml, content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename="helerm-export.xml"'
        return response
