import pytest
from auditlog.models import LogEntry
from django.contrib.auth import get_user_model
from django.utils import timezone


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("last_login", timezone.now()),
        ("last_api_use", timezone.now()),
    ],
)
@pytest.mark.django_db
def test_user_auditlog_excludes_field_updates(field_name, value):
    user = get_user_model().objects.create_user(
        username="auditlog-user", email="auditlog@example.com", password="password"
    )

    setattr(user, field_name, value)
    user.save(update_fields=(field_name,))

    assert (
        LogEntry.objects.filter(
            content_type__app_label="users",
            content_type__model="user",
            object_pk=str(user.pk),
            action=LogEntry.Action.UPDATE,
        ).count()
        == 0
    )


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("first_name", "John"),
        ("last_name", "Doe"),
        ("email", "different@example.com"),
    ],
)
@pytest.mark.django_db
def test_user_auditlog_masks_field_updates(field_name, value):
    user = get_user_model().objects.create_user(
        username="auditlog-user", email="auditlog@example.com", password="password"
    )

    setattr(user, field_name, value)
    user.save(update_fields=(field_name,))

    log_entries = LogEntry.objects.filter(
        content_type__app_label="users",
        content_type__model="user",
        object_pk=str(user.pk),
        action=LogEntry.Action.UPDATE,
    )
    assert log_entries.count() == 1
    assert log_entries[0].changes[field_name] == ["*", "*"]
