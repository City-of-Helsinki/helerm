import os
import uuid
from unittest import mock

import freezegun
import pytest
from lxml import etree
from rest_framework.test import APIClient

import metarecord.exporter.jhs as jhs
from metarecord.exporter.jhs.exporter import JHSExporter, JHSExporterException
from metarecord.models import Function
from metarecord.views.export import JHSExportViewSet


@pytest.fixture
def jhs_export_xml_template(current_directory):
    filename = "jhs_export_template.xml"
    f = open(os.path.join(current_directory, "test_data", filename), "rb")
    yield f
    f.close()


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
def test_exporter_xml_generation_is_successful(
    jhs_export_xml_template, function, phase, action, record
):
    function.state = Function.APPROVED
    function.attributes = {"PublicityClass": "Julkinen"}
    function.save(update_fields=("attributes", "state"))

    mock_uuid = uuid.uuid4()
    with (
        freezegun.freeze_time("2020-04-01 12:00 EEST"),
        mock.patch("uuid.uuid4", return_value=mock_uuid),
    ):
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
def test_exporter_xml_export_is_successful(
    jhs_export_xml_template, function, phase, action, record, tmp_path
):
    function.state = Function.APPROVED
    function.attributes = {"PublicityClass": "Julkinen"}
    function.save(update_fields=("attributes", "state"))
    xml_path = tmp_path / "test.xml"

    mock_uuid = uuid.uuid4()
    with (
        freezegun.freeze_time("2020-04-01 12:00 EEST"),
        mock.patch("uuid.uuid4", return_value=mock_uuid),
    ):
        JHSExporter().export_data(xml_path)

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
        .encode("utf-8")
    )

    with open(xml_path, "rb") as xml:
        assert xml.read() == expected_xml


@pytest.mark.django_db
def test_exporter_xml_export_raises_exception_on_write_error():
    with (
        mock.patch("builtins.open", mock.mock_open()) as mock_file,
        mock.patch("metarecord.exporter.jhs.exporter.JHSExporter.create_xml"),
    ):
        mock_file.return_value.write.side_effect = IOError("Test error")
        with pytest.raises(JHSExporterException):
            JHSExporter().export_data("test.xml")


@pytest.mark.parametrize(
    "initial_attributes, attr_name, jhs_mapping, expected_value",
    [
        ({"foo": None}, "foo", None, None),
        ({"foo": "bar"}, "baz", None, None),
        ({"foo": "bar"}, "foo", None, "bar"),
        ({"foo": "bar"}, "foo", {"foo": {"bar": "mapped"}}, "mapped"),
    ],
)
def test__get_attribute_value_returns_correct_value(
    initial_attributes, attr_name, jhs_mapping, expected_value
):
    """Test that _get_attribute_value returns the correct value in all cases."""
    obj = mock.Mock(attributes=initial_attributes)
    with mock.patch.dict(
        jhs.builder.JHS_MAPPING, jhs_mapping or jhs.builder.JHS_MAPPING
    ):
        assert jhs.builder._get_attribute_value(obj, attr_name) == expected_value


@mock.patch.dict(jhs.builder.JHS_MAPPING, {"foo": {"x": "y"}})
def test__get_attribute_value_raises_exception_when_attribute_not_found():
    """Test that ValueError is raised when attribute is not found."""
    obj = mock.Mock()
    obj.attributes = {"foo": "bar"}

    with pytest.raises(ValueError):
        jhs.builder._get_attribute_value(obj, "foo")


def test_exporter_validate_xml_exception():
    """Test that JHSExporterException is raised when XML is invalid."""
    with pytest.raises(JHSExporterException):
        JHSExporter().validate_xml(etree.tostring(jhs.bindings.E.SomethingWrong()))


def test_tos_attr_returns_prefixed_attribute():
    assert jhs.bindings.tos_attr("foo") == f"{{{jhs.JHS_NAMESPACE}}}foo"


def test_create_wrapped_element():
    """Test that create_wrapped_element creates a wrapped element correctly."""
    foo_el = jhs.bindings.E.Foo
    wrapped_foo_el = jhs.bindings.create_wrapped_element(foo_el)

    wrapped_foo = wrapped_foo_el({"{http://test}foo": "foo"}, bar="bar")

    assert wrapped_foo_el().tag == foo_el().tag
    # Should prefix un-prefixed attributes with the namespace
    assert wrapped_foo.get(jhs.bindings.tos_attr("bar")) == "bar"
    # Should not prefix already prefixed attributes
    assert wrapped_foo.get("{http://test}foo") == "foo"


def test_exporter_create_xml_error_during_build():
    """Test that JHSExporterException is raised when XML is invalid."""
    with mock.patch(
        "metarecord.exporter.jhs.builder.build_tos_document", side_effect=Exception
    ):
        with pytest.raises(JHSExporterException):
            JHSExporter().create_xml()


@pytest.mark.parametrize(
    "xml_declaration, expected",
    [
        (b"", b""),
        (
            b"<?xml version='1.0' encoding='UTF-8'?>",
            b'<?xml version="1.0" encoding="UTF-8"?>',
        ),
        (
            b"<?xml version='1.0' encoding='UTF-8' standalone='yes'?>",
            b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        ),
        (
            b"adsdasdas<?xml version='1.0' encoding='UTF-8'?>",
            b"adsdasdas<?xml version='1.0' encoding='UTF-8'?>",
        ),
    ],
)
def test_fix_xml_declaration(xml_declaration, expected):
    """Test that fix_xml_declaration fixes the XML declaration."""
    assert jhs.exporter.fix_xml_declaration_single_quotes(xml_declaration) == expected
