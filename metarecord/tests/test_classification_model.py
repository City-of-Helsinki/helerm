import pytest

from metarecord.models import Classification


@pytest.mark.django_db
def test__classification__delete_old_unapproved_versions_on_save(classification):
    v1 = classification
    v1.state = Classification.APPROVED
    v1.save()
    assert v1.version == 1

    v1.pk = None
    v1.state = Classification.DRAFT
    v1.save()
    v2 = Classification.objects.latest_version().get(uuid=classification.uuid)
    assert v2.version == 2

    v2.pk = None
    v2.state = Classification.SENT_FOR_REVIEW
    v2.save()
    v3 = Classification.objects.latest_version().get(uuid=classification.uuid)
    assert v3.version == 3

    v3.pk = None
    v3.state = Classification.WAITING_FOR_APPROVAL
    v3.save()
    v4 = Classification.objects.latest_version().get(uuid=classification.uuid)
    assert v4.version == 4

    # Check that nothing has been deleted by mistake so far
    assert Classification.objects.filter(uuid=v1.uuid).count() == 4

    # v5 is approved and saving it should delete all older unapproved versions
    v4.pk = None
    v4.state = Classification.APPROVED
    v4.save()
    v5 = Classification.objects.latest_version().get(uuid=classification.uuid)
    assert v5.version == 5

    assert (
        not Classification.objects.filter(uuid=v5.uuid)
        .exclude(state=Classification.APPROVED)
        .exists()
    )
    assert Classification.objects.count() == 2
