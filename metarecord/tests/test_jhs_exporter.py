import os
import uuid
from unittest import mock

import freezegun
import pytest
from lxml import etree
from rest_framework.test import APIClient

import metarecord.exporter.jhs_v2 as jhs
from metarecord.exporter.jhs import JHSExporter
from metarecord.exporter.jhs_v2.exporter import JHSExporterV2, JHSExporterV2Exception
from metarecord.models import Function
from metarecord.views.export import JHSExportViewSet


@pytest.fixture
def jhs_export_xml_template(current_directory):
    filename = "jhs_export_template.xml"
    f = open(os.path.join(current_directory, "test_data", filename), "rb")
    yield f
    f.close()


@pytest.fixture
def jhs_export_xml_template_lxml(current_directory):
    filename = "jhs_export_template_lxml.xml"
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


@pytest.mark.django_db
def test_lxml_exporter_xml_generation_is_successful(
    jhs_export_xml_template_lxml, function, phase, action, record
):
    function.state = Function.APPROVED
    function.save(update_fields=("attributes", "state"))

    with freezegun.freeze_time("2020-04-01 12:00 EEST"):
        mock_uuid = uuid.uuid4()

        with mock.patch("uuid.uuid4", return_value=mock_uuid):
            xml = JHSExporterV2().create_xml().decode("utf-8")

    expected_xml = (
        jhs_export_xml_template_lxml.read()
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


def test_lxml_exporter_validate_xml_exception():
    """Test that JHSExporterV2Exception is raised when XML is invalid."""
    with pytest.raises(JHSExporterV2Exception):
        JHSExporterV2().validate_xml(etree.tostring(jhs.bindings.E.SomethingWrong()))


def test_tos_attr_returns_prefixed_attribute():
    assert jhs.bindings.tos_attr("foo") == f"{{{jhs.JHS_NAMESPACE}}}foo"


def test_create_wrapped_element():
    """Test that create_wrapped_element creates a wrapped element correctly."""
    FOO = jhs.bindings.E.Foo
    WRAPPED_FOO = jhs.bindings.create_wrapped_element(FOO)

    wrapped_foo = WRAPPED_FOO({"{http://test}foo": "foo"}, bar="bar")

    assert WRAPPED_FOO().tag == FOO().tag
    # Should prefix un-prefixed attributes with the namespace
    assert wrapped_foo.get(jhs.bindings.tos_attr("bar")) == "bar"
    # Should not prefix already prefixed attributes
    assert wrapped_foo.get("{http://test}foo") == "foo"


def test_lxml_exporter_create_xml_error_during_build():
    """Test that JHSExporterV2Exception is raised when XML is invalid."""
    with mock.patch(
        "metarecord.exporter.jhs_v2.builder.build_tos_document", side_effect=Exception
    ):
        with pytest.raises(JHSExporterV2Exception):
            JHSExporterV2().create_xml()
