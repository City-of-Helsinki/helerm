import pytest

from metarecord.models import Classification, Function


@pytest.mark.django_db
def test_function_get_name(function):
    assert function.get_name() == function.classification.title

    function.is_template = True
    function.save(update_fields=("is_template",))

    assert function.get_name() == function.name


@pytest.mark.django_db
def test_function_draft_delete(function):
    function.state = Function.APPROVED
    can_delete = function.can_user_delete(None)
    assert can_delete is False


@pytest.mark.django_db
def test_function_save_without_classification(function):
    function.classification = None
    with pytest.raises(Exception) as excinfo:
        function.save()
    assert str(excinfo.value) == "Classification is required."


@pytest.mark.django_db
def test_approved_function_with_unapproved_classification(function):
    function.state = Function.APPROVED
    function.classification.state = Classification.DRAFT
    with pytest.raises(Exception) as excinfo:
        function.save()
    assert str(excinfo.value) == "Approved function must have approved classification"


@pytest.mark.django_db
def test_function_unapproved_delete_old_versions(function):
    with pytest.raises(Exception) as excinfo:
        function.delete_old_non_approved_versions()
    assert str(excinfo.value) == "Function must be approved before old non-approved versions can be deleted."
