import logging
from io import BytesIO

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.utils.translation import gettext as _

from metarecord.importer.tos import TOSImporter


class CaptureLogRecordsHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_records = []

    def emit(self, record):
        self.log_records.append(record)


def tos_import_view(request, context: dict = None):
    context = context or {}
    if not (request.user.is_authenticated and request.user.is_superuser):
        raise PermissionDenied

    if request.method == "POST":
        importer = TOSImporter()
        logger = logging.getLogger("tos_import_capture_logger")
        logger.setLevel(logging.DEBUG)
        handler = CaptureLogRecordsHandler()
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        importer.logger = logger
        filename = ""

        try:
            data = request.FILES["tosfile"].read()
            filename = request.FILES["tosfile"].name
            importer.open(BytesIO(data))
            importer.import_data()
            messages.add_message(
                request,
                messages.INFO,
                _('File "%s" was imported successfully!') % filename,
            )
        except Exception as e:
            messages.add_message(
                request, messages.ERROR, _('Error importing file "%s"') % filename
            )
            logger.error(e)

        context["logs"] = handler.log_records

    return render(request, "admin/metarecord/function/import_tos.html", context)
