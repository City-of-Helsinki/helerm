import pytest
from auditlog.models import LogEntry

from metarecord.models import Classification


@pytest.mark.django_db
def test_log_entry_created_when_classification_is_created():
    classification = Classification.objects.create(
        title="test classification", code="99", function_allowed=False
    )

    assert (
        LogEntry.objects.filter(
            content_type__app_label="metarecord",
            content_type__model="classification",
            object_pk=str(classification.pk),
            action=LogEntry.Action.CREATE,
        ).count()
        == 1
    )


@pytest.mark.django_db
def test_log_entry_created_when_classification_is_updated():
    classification = Classification.objects.create(
        title="test classification", code="98", function_allowed=False
    )

    classification.title = "updated classification"
    classification.save(update_fields=("title",))

    assert (
        LogEntry.objects.filter(
            content_type__app_label="metarecord",
            content_type__model="classification",
            object_pk=str(classification.pk),
            action=LogEntry.Action.UPDATE,
        ).count()
        == 1
    )


@pytest.mark.django_db
def test_log_entry_created_when_classification_is_deleted():
    classification = Classification.objects.create(
        title="test classification", code="97", function_allowed=False
    )
    classification_pk = str(classification.pk)

    classification.delete()

    assert (
        LogEntry.objects.filter(
            content_type__app_label="metarecord",
            content_type__model="classification",
            object_pk=classification_pk,
            action=LogEntry.Action.DELETE,
        ).count()
        == 1
    )
