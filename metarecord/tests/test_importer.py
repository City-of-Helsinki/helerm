import pytest

from metarecord.importer.tos import TOSImporter, TOSImporterException


@pytest.mark.django_db
def test_tos_importer_with_no_classification(tos_importer_excel_file_path):
    tos_importer = TOSImporter()
    tos_importer.open(tos_importer_excel_file_path)
    with pytest.raises(TOSImporterException) as excinfo:
        tos_importer.import_data()
    assert str(excinfo.value) == "Classification 00 00 01 02 does not exist"


@pytest.mark.django_db
def test_tos_importer_with_classification_and_function(function, tos_importer_excel_file_path):
    function.classification.code = "00 00 01 02"
    function.classification.save(update_fields=["code"])

    tos_importer = TOSImporter()
    tos_importer.open(tos_importer_excel_file_path)

    tos_importer.import_data()
    tos_importer.import_attributes()
