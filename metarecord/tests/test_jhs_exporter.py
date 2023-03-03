import os
import uuid
from unittest import mock

import freezegun
import pytest
from rest_framework.test import APIClient

from metarecord.exporter.jhs import JHSExporter
from metarecord.models import Function
from metarecord.views.export import JHSExportViewSet


@pytest.fixture
def jhs_export_xml_template(current_directory):
    filename = "jhs_export_template.xml"
    f = open(os.path.join(current_directory, "test_data", filename), "rb")
    yield f
    f.close()


@pytest.mark.django_db
def test_exporter_xml_generation_is_successful(
    jhs_export_xml_template, function, phase, action, record
):
    function.state = Function.APPROVED
    function.save(update_fields=("attributes", "state"))

    with freezegun.freeze_time("2020-04-01 12:00 EEST"):
        mock_uuid = uuid.uuid4()

        with mock.patch("uuid.uuid4", return_value=mock_uuid):
            xml = JHSExporter().create_xml().decode("utf-8")

    expected_xml = (
        jhs_export_xml_template.read()
        .decode("utf-8")
        .format(
            id=mock_uuid,
            func_id=function.uuid,
            phase_id=phase.uuid,
            action_id=action.uuid,
            rec_id=record.uuid,
        )
    )

    assert xml == expected_xml


@pytest.mark.django_db
def test_export_view_file_creation(function, phase, action, record):
    client = APIClient()
    response = client.get("/export/")
    assert "Content-Disposition" in response


@pytest.mark.django_db
def test_jhs_export_view_file_creation(function, phase, action, record):
    jhs_export_view = JHSExportViewSet()

    open_mock = mock.mock_open()
    open_mock.side_effect = [FileNotFoundError, mock.DEFAULT]
    with mock.patch("metarecord.views.export.open", open_mock, create=True):
        response = jhs_export_view.list(None)

    open_mock.assert_called()
    open_mock.return_value.write.assert_called_once()
    assert "Content-Disposition" in response
