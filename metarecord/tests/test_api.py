import datetime
import json
import uuid
from unittest import mock

import freezegun
import pytest
import pytz
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse

from metarecord.models import Action, Classification, Function, Phase, Record
from metarecord.models.bulk_update import BulkUpdate
from metarecord.tests.utils import (
    assert_response_functions,
    check_attribute_errors,
    FunctionTestDetailSerializer,
    get_bulk_update_function_key,
    set_permissions,
)
from metarecord.views.classification import include_related

CLASSIFICATION_LIST_URL = reverse("classification-list")
FUNCTION_LIST_URL = reverse("function-list")
ATTRIBUTE_LIST_URL = reverse("attribute-list")
BULK_UPDATE_LIST_URL = reverse("bulkupdate-list")
PATCH_FIELDS = ("valid_from", "valid_to", "state")


def get_classification_detail_url(classification):
    return reverse("classification-detail", kwargs={"uuid": classification.uuid})


def get_function_detail_url(function):
    return reverse("function-detail", kwargs={"uuid": function.uuid})


def get_attribute_detail_url(attribute):
    return reverse("attribute-detail", kwargs={"pk": attribute.id})


def get_bulk_update_detail_url(bulk_update):
    return reverse("bulkupdate-detail", kwargs={"pk": bulk_update.pk})


def get_bulk_update_approve_url(bulk_update):
    return reverse("bulkupdate-approve", kwargs={"pk": bulk_update.pk})


def get_record_detail_url(record):
    return reverse("record-detail", kwargs={"uuid": record.uuid})


@pytest.fixture
def post_function_data(classification, free_text_attribute, choice_attribute):
    return {
        "classification": {
            "id": classification.uuid.hex,
            "version": classification.version,
        },
        "attributes": {
            free_text_attribute.identifier: "new function attribute value",
        },
        "phases": [
            {
                "actions": [
                    {
                        "records": [
                            {
                                "attributes": {
                                    choice_attribute.identifier: "new record attribute value",
                                },
                            }
                        ]
                    }
                ]
            }
        ],
        "state": "sent_for_review",  # should be ignored
        "version": 7,  # should be ignored
    }


@pytest.fixture
def put_function_data(function, free_text_attribute, choice_attribute, bulk_update):
    return {
        "name": "new function version",
        "function_id": function.classification.code,
        "parent": "xyz",
        "classification": {
            "id": function.classification.uuid.hex,
            "version": function.classification.version,
        },
        "attributes": {
            free_text_attribute.identifier: "new function version attribute value",
        },
        "phases": [
            {
                "actions": [
                    {
                        "records": [
                            {
                                "attributes": {
                                    choice_attribute.identifier: "new function version record attribute value",
                                },
                            }
                        ]
                    }
                ]
            }
        ],
        "bulk_update": bulk_update.id,
    }


# by default disable hardcoded attribute validations so that they don't interfere
# in tests unrelated to attribute validation, attribute validations are tested
# explicitly in their own tests.
@pytest.fixture(autouse=True)
def disable_attribute_validations(monkeypatch):
    _attribute_validations = {
        "allowed": None,
        "required": None,
        "conditionally_required": None,
        "multivalued": None,
        "all_or_none": None,
    }

    for structural_element in (Function, Phase, Action, Record):
        monkeypatch.setattr(
            structural_element, "_attribute_validations", _attribute_validations
        )


def _check_function_object_matches_data(function_obj, data):
    new_function = function_obj

    assert new_function.attributes == data["attributes"]
    assert new_function.phases.count() == 1

    new_phase = new_function.phases.first()
    phase_data = data["phases"][0]
    assert new_phase.attributes == {}
    assert new_phase.actions.count() == 1

    new_action = new_phase.actions.first()
    action_data = phase_data["actions"][0]
    assert new_action.attributes == {}
    assert new_action.records.count() == 1

    new_record = new_action.records.first()
    record_data = action_data["records"][0]
    assert new_record.attributes == record_data["attributes"]


@pytest.fixture
def attribute(choice_attribute):
    return choice_attribute


@pytest.mark.parametrize(
    "resource",
    [
        "function",
        "attribute",
        "template",
        "classification",
    ],
)
@pytest.mark.django_db
def test_get(
    api_client,
    resource,
    function,
    phase,
    action,
    record,
    attribute,
    template,
    classification,
):
    """
    Test GET to every resource's list and detail endpoint.
    """
    function.state = Function.APPROVED
    function.save(update_fields=("state",))

    list_url = reverse("%s-list" % resource)
    response = api_client.get(list_url)
    assert response.status_code == 200
    assert len(response.data["results"])

    id_field = "pk" if resource == "attribute" else "uuid"
    id_value = getattr(locals().get(resource), id_field)
    detail_url = reverse(
        "%s-detail" % resource.replace("_", ""), kwargs={id_field: id_value}
    )
    response = api_client.get(detail_url)
    assert response.status_code == 200
    assert response.data


@pytest.mark.django_db
def test_get_attribute_schemas(api_client):
    url = "{}schemas/".format(reverse("attribute-list"))
    response = api_client.get(url)
    assert response.status_code == 200

    for element in ("function", "phase", "action", "record"):
        assert len(response.data.get(element))


@pytest.mark.django_db
def test_function_versioning(user_api_client, classification, classification_2):
    first_draft = Function.objects.create(
        classification=classification, attributes={"subject": "first draft"}
    )
    first_approved = Function.objects.create(
        classification=classification,
        state=Function.APPROVED,
        attributes={"subject": "first approved"},
    )
    second_approved = Function.objects.create(
        classification=classification,
        state=Function.APPROVED,
        attributes={"subject": "second approved"},
    )
    second_draft = Function.objects.create(
        classification=classification, attributes={"subject": "second draft"}
    )
    other_function = Function.objects.create(
        classification=classification_2, attributes={"subject": "other function"}
    )
    template = Function.objects.create(
        is_template=True, attributes={"subject": "template"}
    )

    assert (
        first_draft.uuid
        == first_approved.uuid
        == second_approved.uuid
        == second_draft.uuid
    )
    assert first_draft.version == 1
    assert first_approved.version == 2
    assert second_approved.version == 3
    assert second_draft.version == 4
    assert other_function.version == 1
    assert template.version is None

    url = reverse("function-detail", kwargs={"uuid": first_draft.uuid})

    # /function/<uuid>/ should return the latest version
    response = user_api_client.get(url)
    assert response.status_code == 200
    assert response.data["attributes"]["subject"] == "second draft"

    # /function/<uuid>/?state=approved should return the latest approved version
    response = user_api_client.get(url + "?state=approved")
    assert response.status_code == 200
    assert response.data["attributes"]["subject"] == "second approved"


@pytest.mark.django_db
def test_unauthenticated_user_cannot_post_or_put_functions(
    post_function_data, put_function_data, api_client, function
):
    response = api_client.post(FUNCTION_LIST_URL, data=post_function_data)
    assert response.status_code == 401

    response = api_client.put(get_function_detail_url(function), data=put_function_data)
    assert response.status_code == 401


@pytest.mark.django_db
def test_function_post_requires_edit_permission(post_function_data, user_api_client):
    response = user_api_client.post(FUNCTION_LIST_URL, data=post_function_data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_function_post(post_function_data, user_api_client):
    set_permissions(user_api_client, Function.CAN_EDIT)

    response = user_api_client.post(FUNCTION_LIST_URL, data=post_function_data)
    assert response.status_code == 201

    new_function = Function.objects.last()

    _check_function_object_matches_data(new_function, post_function_data)

    assert new_function.state == Function.DRAFT
    assert new_function.version == 1
    assert new_function.metadata_versions.count() == 1
    assert new_function.modified_by == user_api_client.user
    metadata_version = new_function.metadata_versions.last()
    assert metadata_version.state == Function.DRAFT

    assert (
        response.data["name"]
        == response.data["classification_title"]
        == new_function.classification.title
    )
    assert (
        response.data["function_id"]
        == response.data["classification_code"]
        == new_function.classification.code
    )


@pytest.mark.django_db
def test_function_post_with_multiple_available_classification_versions(
    post_function_data, classification, user_api_client
):
    """
    Test that creating new function will set classification relation to the correct version
    specified in request data
    """
    set_permissions(user_api_client, Function.CAN_EDIT)
    classification_v2 = Classification.objects.create(
        uuid=classification.uuid,
        title="test classification v2",
        code=classification.code,
        function_allowed=classification.function_allowed,
    )

    post_function_data["classification"]["version"] = classification_v2.version

    response = user_api_client.post(FUNCTION_LIST_URL, data=post_function_data)

    assert response.status_code == 201
    new_function = Function.objects.last()
    assert new_function.classification == classification_v2


@pytest.mark.django_db
def test_function_post_empty_function(user_api_client, classification):
    set_permissions(user_api_client, Function.CAN_EDIT)
    response = user_api_client.post(
        FUNCTION_LIST_URL,
        data={
            "classification": {
                "id": classification.uuid.hex,
                "version": classification.version,
            },
        },
    )
    assert response.status_code == 201

    new_function = Function.objects.last()
    assert not new_function.phases.exists()
    assert new_function.attributes == {}
    assert new_function.state == Function.DRAFT
    assert new_function.version == 1
    assert new_function.metadata_versions.count() == 1
    metadata_version = new_function.metadata_versions.last()
    assert metadata_version.state == Function.DRAFT

    assert (
        response.data["name"]
        == response.data["classification_title"]
        == new_function.classification.title
    )
    assert (
        response.data["function_id"]
        == response.data["classification_code"]
        == new_function.classification.code
    )


@pytest.mark.django_db
def test_cannot_post_more_than_one_function_for_classification(
    post_function_data, user_api_client
):
    set_permissions(user_api_client, Function.CAN_EDIT)

    response = user_api_client.post(FUNCTION_LIST_URL, data=post_function_data)
    assert response.status_code == 201

    response = user_api_client.post(FUNCTION_LIST_URL, data=post_function_data)
    assert response.status_code == 400
    assert "Classification %s already has a function." % post_function_data[
        "classification"
    ]["id"] in str(response.data)


@pytest.mark.django_db
def test_function_put(
    put_function_data, user_api_client, function, phase, action, record
):
    set_permissions(user_api_client, Function.CAN_EDIT)

    models = (function, phase, action, record)
    modified_ats = [
        obj.modified_at for obj in models
    ]  # store original modified_at timestamps

    response = user_api_client.put(
        get_function_detail_url(function), data=put_function_data
    )
    assert response.status_code == 200

    new_function = Function.objects.last()
    _check_function_object_matches_data(new_function, put_function_data)

    assert new_function.version == 2
    assert new_function.uuid == function.uuid

    # check that the original objects haven't been modified
    for index, obj in enumerate(models):
        obj.refresh_from_db()
        assert obj.modified_at == modified_ats[index]


@pytest.mark.django_db
def test_function_put_with_new_classification_version(
    put_function_data, user_api_client, classification, function
):
    set_permissions(user_api_client, Function.CAN_EDIT)
    classification_v2 = Classification.objects.create(
        uuid=classification.uuid,
        title="test classification v2",
        code=classification.code,
        function_allowed=classification.function_allowed,
    )
    # Sanity checks before writing anything
    assert function.classification.title == classification.title
    assert function.classification.version == classification.version
    assert classification_v2.version == 2
    put_function_data["classification"] = {
        "id": classification_v2.uuid.hex,
        "version": classification_v2.version,
    }

    response = user_api_client.put(
        get_function_detail_url(function), data=put_function_data
    )
    assert response.status_code == 200

    new_function = Function.objects.latest_version().get(uuid=function.uuid)
    _check_function_object_matches_data(new_function, put_function_data)
    assert Function.objects.count() == 2
    assert new_function.uuid == function.uuid
    assert new_function.classification.title == classification_v2.title
    assert new_function.classification.version == classification_v2.version


@pytest.mark.django_db
def test_function_post_invalid_attributes(post_function_data, user_api_client):
    post_function_data["attributes"] = {"InvalidFunctionAttribute": "value"}
    post_function_data["phases"][0]["attributes"] = {"InvalidPhaseAttribute": "value"}

    response = user_api_client.post(FUNCTION_LIST_URL, data=post_function_data)
    assert response.status_code == 400
    assert response.data["attributes"]["InvalidFunctionAttribute"] == [
        "Invalid attribute."
    ]
    assert response.data["phases"][0]["attributes"]["InvalidPhaseAttribute"] == [
        "Invalid attribute."
    ]


@pytest.mark.django_db
def test_function_put_invalid_attributes(put_function_data, user_api_client, function):
    put_function_data["function_id"] = function.classification.code
    put_function_data["attributes"] = {"InvalidFunctionAttribute": "value"}
    put_function_data["phases"][0]["attributes"] = {"InvalidPhaseAttribute": "value"}

    response = user_api_client.put(
        get_function_detail_url(function), data=put_function_data
    )
    assert response.status_code == 400
    assert response.data["attributes"]["InvalidFunctionAttribute"] == [
        "Invalid attribute."
    ]
    assert response.data["phases"][0]["attributes"]["InvalidPhaseAttribute"] == [
        "Invalid attribute."
    ]


@pytest.mark.django_db
def test_function_put_not_able_to_change_classification(
    put_function_data, user_api_client, function, classification, classification_2
):
    set_permissions(user_api_client, Function.CAN_EDIT)
    put_function_data["classification"] = {
        "id": classification_2.uuid.hex,
        "version": classification_2.version,
    }

    response = user_api_client.put(
        get_function_detail_url(function), data=put_function_data
    )

    assert response.status_code == 400
    latest_version = (
        Function.objects.filter(uuid=function.uuid).latest_version().first()
    )
    assert latest_version.version == function.version
    assert response.json() == {
        "non_field_errors": [
            "Changing classification is not allowed. Only version can be changed."
        ]
    }


@pytest.mark.django_db
def test_function_multivalued_attribute(
    monkeypatch, put_function_data, user_api_client, function, free_text_attribute
):
    set_permissions(user_api_client, Function.CAN_EDIT)

    monkeypatch.setitem(
        Function._attribute_validations, "multivalued", [free_text_attribute.identifier]
    )

    put_function_data["function_id"] = function.classification.code
    put_function_data["attributes"] = {
        free_text_attribute.identifier: ["value1", "value2"]
    }

    response = user_api_client.put(
        get_function_detail_url(function), data=put_function_data
    )
    assert response.status_code == 200

    put_function_data["state"] = Function.SENT_FOR_REVIEW
    response = user_api_client.patch(
        get_function_detail_url(function), data=put_function_data
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_function_multivalued_attribute_allow_single(
    monkeypatch, put_function_data, user_api_client, function, free_text_attribute
):
    set_permissions(user_api_client, Function.CAN_EDIT)

    monkeypatch.setitem(
        Function._attribute_validations, "multivalued", [free_text_attribute.identifier]
    )

    put_function_data["function_id"] = function.classification.code
    put_function_data["attributes"] = {free_text_attribute.identifier: "value1"}

    response = user_api_client.put(
        get_function_detail_url(function), data=put_function_data
    )
    assert response.status_code == 200

    put_function_data["state"] = Function.SENT_FOR_REVIEW
    response = user_api_client.patch(
        get_function_detail_url(function), data=put_function_data
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_function_multivalued_attribute_not_allowed(
    put_function_data, user_api_client, function, free_text_attribute
):
    set_permissions(user_api_client, Function.CAN_EDIT)

    put_function_data["function_id"] = function.classification.code
    put_function_data["attributes"] = {
        free_text_attribute.identifier: ["value1", "value2"]
    }

    response = user_api_client.put(
        get_function_detail_url(function), data=put_function_data
    )
    assert response.status_code == 200

    put_function_data["state"] = Function.SENT_FOR_REVIEW
    response = user_api_client.patch(
        get_function_detail_url(function), data=put_function_data
    )
    assert response.status_code == 400
    assert response.data["attributes"][free_text_attribute.identifier] == [
        "This attribute does not allow multiple values."
    ]


@pytest.mark.parametrize(
    "attributes",
    [
        "foo",
        ["foo"],
    ],
)
@pytest.mark.django_db
def test_function_put_invalid_attributes_format(
    put_function_data, user_api_client, function, attributes
):
    put_function_data["function_id"] = function.classification.code
    put_function_data["phases"][0]["attributes"] = attributes
    response = user_api_client.put(
        get_function_detail_url(function), data=put_function_data
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_function_state_change(user_api_client, function):
    set_permissions(user_api_client, Function.CAN_EDIT)
    data = {"state": Function.SENT_FOR_REVIEW, "name": "this should be ignored"}

    response = user_api_client.patch(get_function_detail_url(function), data=data)
    assert response.status_code == 200
    assert response.data["version"] == 1
    assert response.data["state"] == Function.SENT_FOR_REVIEW

    function.refresh_from_db()
    assert function.version == 1
    assert function.state == Function.SENT_FOR_REVIEW


@pytest.mark.django_db
def test_function_put_state(put_function_data, user_api_client, function):
    set_permissions(user_api_client, Function.CAN_EDIT)
    put_function_data["state"] = Function.SENT_FOR_REVIEW

    response = user_api_client.put(
        get_function_detail_url(function), data=put_function_data
    )
    assert response.status_code == 200

    new_function = Function.objects.last()
    assert new_function.state == Function.DRAFT


@pytest.mark.django_db
def test_state_change_validity(user_api_client, function):
    set_permissions(
        user_api_client,
        (
            Function.CAN_EDIT,
            Function.CAN_REVIEW,
            Function.CAN_APPROVE,
            "metarecord.delete_function",
        ),
    )
    url = get_function_detail_url(function)

    all_states = {
        Function.DRAFT,
        Function.SENT_FOR_REVIEW,
        Function.WAITING_FOR_APPROVAL,
        Function.APPROVED,
    }

    valid_changes = {
        Function.DRAFT: {Function.SENT_FOR_REVIEW},
        Function.SENT_FOR_REVIEW: {Function.WAITING_FOR_APPROVAL, Function.DRAFT},
        Function.WAITING_FOR_APPROVAL: {Function.APPROVED, Function.DRAFT},
        Function.APPROVED: {Function.DRAFT},
    }

    for old_state, valid_new_states in valid_changes.items():
        function.state = old_state
        function.save(update_fields=("state",))

        for new_state in valid_new_states:
            function.state = old_state
            function.save(update_fields=("state",))

            response = user_api_client.patch(url, data={"state": new_state})
            assert response.status_code == 200

        invalid_new_states = all_states - valid_new_states - {old_state}

        for new_state in invalid_new_states:
            function.state = old_state
            function.save(update_fields=("state",))

            response = user_api_client.patch(url, data={"state": new_state})
            assert response.status_code == 400


@pytest.mark.django_db
def test_state_change_permissions(user_api_client, function):
    url = get_function_detail_url(function)

    all_permissions = {Function.CAN_EDIT, Function.CAN_REVIEW, Function.CAN_APPROVE}

    required_perms = {
        Function.SENT_FOR_REVIEW: Function.CAN_EDIT,
        Function.WAITING_FOR_APPROVAL: Function.CAN_REVIEW,
        Function.APPROVED: Function.CAN_APPROVE,
    }

    valid_changes = {
        Function.DRAFT: Function.SENT_FOR_REVIEW,
        Function.SENT_FOR_REVIEW: Function.WAITING_FOR_APPROVAL,
        Function.WAITING_FOR_APPROVAL: Function.APPROVED,
    }

    # forward changes
    for old_state, new_state in valid_changes.items():
        function.state = old_state
        function.save(update_fields=("state",))
        required_perm = required_perms[new_state]

        others_than_required_perm = all_permissions - {required_perm}
        set_permissions(user_api_client, others_than_required_perm)
        response = user_api_client.patch(url, data={"state": new_state})
        assert response.status_code == 403

        set_permissions(user_api_client, required_perm)
        response = user_api_client.patch(url, data={"state": new_state})
        assert response.status_code == 200

    # changes back to DRAFT
    for old_state in {
        Function.SENT_FOR_REVIEW,
        Function.WAITING_FOR_APPROVAL,
        Function.APPROVED,
    }:
        function.state = old_state
        function.save(update_fields=("state",))
        required_perm = required_perms[old_state]

        others_than_required_perm = all_permissions - {required_perm}
        set_permissions(user_api_client, others_than_required_perm)
        response = user_api_client.patch(url, data={"state": Function.DRAFT})
        assert response.status_code == 403

        set_permissions(user_api_client, required_perm)
        response = user_api_client.patch(url, data={"state": Function.DRAFT})
        assert response.status_code == 200


@pytest.mark.django_db
def test_metadata_version(
    user_api_client, user_2_api_client, function, put_function_data
):
    url = get_function_detail_url(function)
    set_permissions(user_api_client, Function.CAN_EDIT)
    set_permissions(user_2_api_client, Function.CAN_EDIT)
    put_function_data["valid_from"] = "2015-01-01"

    response = user_api_client.put(url, data=put_function_data)
    assert response.status_code == 200

    new_function = Function.objects.last()
    original_modified_at = new_function.modified_at
    assert new_function.metadata_versions.count() == 1
    metadata_version = new_function.metadata_versions.last()
    assert metadata_version.state == Function.DRAFT
    assert metadata_version.modified_at == original_modified_at
    assert metadata_version.modified_by == user_api_client.user
    assert metadata_version._modified_by == "John Rambo"
    assert metadata_version.valid_from == datetime.date(2015, 1, 1)
    assert metadata_version.valid_to is None

    response = user_2_api_client.patch(
        url, data={"state": Function.SENT_FOR_REVIEW, "valid_to": "2016-01-01"}
    )
    assert response.status_code == 200

    new_function = Function.objects.last()
    assert new_function.metadata_versions.count() == 2
    metadata_version = new_function.metadata_versions.last()
    assert metadata_version.state == Function.SENT_FOR_REVIEW
    assert (
        metadata_version.modified_at == new_function.modified_at > original_modified_at
    )
    assert metadata_version.modified_by == user_2_api_client.user
    assert metadata_version._modified_by == "Rocky Balboa"
    assert metadata_version.valid_from == datetime.date(2015, 1, 1)
    assert metadata_version.valid_to == datetime.date(2016, 1, 1)
    assert new_function.modified_by == user_2_api_client.user


@pytest.mark.django_db
def test_metadata_version_modified_by(user, function):
    function.modified_by = user
    function.create_metadata_version()

    metadata_version = function.metadata_versions.first()
    assert metadata_version.modified_by == user
    assert metadata_version._modified_by == "John Rambo"

    user.delete()
    metadata_version.refresh_from_db()
    metadata_version.save()  # Save should not affect _modified_by content
    assert not metadata_version.modified_by
    assert metadata_version._modified_by == "John Rambo"


@pytest.mark.django_db
def test_function_put_no_permission(put_function_data, user_api_client, function):
    response = user_api_client.put(
        get_function_detail_url(function), data=put_function_data
    )
    assert response.status_code == 403
    assert "No permission to edit." in str(response.data)


@pytest.mark.django_db
def test_function_cannot_edit_states(put_function_data, user_api_client, function):
    set_permissions(user_api_client, Function.CAN_EDIT)

    for state in (Function.SENT_FOR_REVIEW, Function.WAITING_FOR_APPROVAL):
        function.state = state
        function.save(update_fields=("state",))

        response = user_api_client.put(
            get_function_detail_url(function), data=put_function_data
        )
        assert response.status_code == 400
        assert "Cannot edit while in state" in str(response.data)


@pytest.mark.django_db
def test_function_modified_by(function, user_api_client, user):
    set_permissions(user_api_client, Function.CAN_VIEW_MODIFIED_BY)

    response = user_api_client.get(get_function_detail_url(function))
    assert response.status_code == 200
    assert response.data["modified_by"] is None

    function.modified_by = user
    function.save()

    response = user_api_client.get(get_function_detail_url(function))
    assert response.status_code == 200
    assert response.data["modified_by"] == "%s %s" % (user.first_name, user.last_name)


@pytest.mark.django_db
def test_function_anonymous_cannot_view_modified_by(function, api_client, user):
    function.state = Function.APPROVED
    function.modified_by = user
    function.save()

    response = api_client.get(get_function_detail_url(function))
    assert response.status_code == 200
    assert "modified_by" not in response.data


@pytest.mark.django_db
def test_function_user_cannot_view_modified_by(function, user_api_client, user):
    function.modified_by = user
    function.save()

    response = user_api_client.get(get_function_detail_url(function))
    assert response.status_code == 200
    assert "modified_by" not in response.data


@pytest.mark.django_db
def test_function_another_user_cannot_view_modified_by(
    function, user_2_api_client, user
):
    function.modified_by = user
    function.save()

    response = user_2_api_client.get(get_function_detail_url(function))
    assert response.status_code == 200
    assert "modified_by" not in response.data


@pytest.mark.django_db
def test_function_anonymous_user_cannot_delete(put_function_data, api_client, function):
    response = api_client.delete(get_function_detail_url(function))
    assert response.status_code == 401


@pytest.mark.django_db
def test_function_user_cannot_delete(put_function_data, user_api_client, function):
    response = user_api_client.delete(get_function_detail_url(function))
    assert response.status_code == 403


@pytest.mark.django_db
def test_function_user_can_delete_own(
    put_function_data, user, user_api_client, function
):
    function.modified_by = user
    function.save()

    response = user_api_client.delete(get_function_detail_url(function))
    assert response.status_code == 204

    with pytest.raises(Function.DoesNotExist):
        Function.objects.get(pk=function.id)


@pytest.mark.django_db
def test_function_user_cannot_delete_other_users(
    put_function_data, user_2, user_api_client, function
):
    function.modified_by = user_2
    function.save()

    response = user_api_client.delete(get_function_detail_url(function))
    assert response.status_code == 403

    new_function = Function.objects.get(pk=function.id)
    assert new_function.state == Function.DRAFT


@pytest.mark.django_db
def test_function_super_user_can_delete(
    put_function_data, super_user_api_client, function
):
    response = super_user_api_client.delete(get_function_detail_url(function))
    assert response.status_code == 204

    with pytest.raises(Function.DoesNotExist):
        Function.objects.get(pk=function.id)


@pytest.mark.django_db
def test_attribute_get_list_and_detail(
    choice_attribute, choice_value_1, attribute_group, user_api_client
):
    for url in (ATTRIBUTE_LIST_URL, get_attribute_detail_url(choice_attribute)):
        response = user_api_client.get(url)
        assert response.status_code == 200
        data = (
            response.data["results"][0] if "results" in response.data else response.data
        )

        assert uuid.UUID(data["id"]) == choice_attribute.id
        assert data["identifier"] == choice_attribute.identifier
        assert data["name"] == choice_attribute.name
        assert data["group"] == attribute_group.name

        assert len(data["values"]) == 1
        value_datum = data["values"][0]
        assert uuid.UUID(value_datum["id"]) == choice_value_1.id
        assert value_datum["value"] == choice_value_1.value
        assert value_datum["name"] == choice_value_1.name
        assert value_datum["help_text"] == choice_value_1.help_text


@pytest.mark.django_db
def test_attribute_validations_when_sent_for_review(
    super_user_api_client,
    function,
    phase,
    action,
    record,
    free_text_attribute,
    free_text_attribute_2,
    choice_attribute,
    choice_value_1,
    choice_value_2,
    choice_attribute_2,
    choice_value_2_1,
    choice_value_2_2,
):
    # set free text attribute required and choice attribute allowed for every structural element
    for structural_element in (Function, Phase, Action, Record):
        structural_element._attribute_validations["allowed"] = [
            free_text_attribute.identifier,
            choice_attribute.identifier,
            choice_attribute_2.identifier,
        ]
        structural_element._attribute_validations["required"] = [
            free_text_attribute.identifier
        ]
        structural_element._attribute_validations["conditionally_required"] = {
            choice_attribute_2.identifier: {
                choice_attribute.identifier: choice_value_2.value
            }
        }

    valid_attributes = {
        free_text_attribute.identifier: "some value",
        choice_attribute.identifier: choice_value_1.value,
    }

    # the function is missing a conditionally required attribute
    function.attributes = {choice_attribute.identifier: choice_value_2.value}
    function.save(update_fields=("attributes",))

    # new phase with valid attributes
    Phase.objects.create(function=function, index=2, attributes=valid_attributes)

    # the action has a non allowed attribute
    action.attributes = {free_text_attribute_2.identifier: "some value"}
    action.save(update_fields=("attributes",))

    # the record has a non allowed value
    record.attributes = {choice_attribute.identifier: choice_value_2_1.value}
    record.save(update_fields=("attributes",))

    # try to send the function for review
    response = super_user_api_client.patch(
        get_function_detail_url(function), data={"state": Function.SENT_FOR_REVIEW}
    )
    assert response.status_code == 400
    errors = response.data

    # check function attribute errors
    check_attribute_errors(errors, free_text_attribute, "required")
    check_attribute_errors(
        errors, choice_attribute_2, "required"
    )  # this should be the conditionally required one

    # check phase attribute errors
    assert (
        errors["phases"][1] == {}
    )  # this should be the new phase with valid attributes
    errors = errors["phases"][0]
    check_attribute_errors(errors, free_text_attribute, "required")

    # check action attribute errors
    errors = errors["actions"][0]
    check_attribute_errors(errors, free_text_attribute, "required")
    check_attribute_errors(errors, free_text_attribute_2, "allowed")

    # check record attribute errors
    errors = errors["records"][0]
    check_attribute_errors(errors, free_text_attribute, "required")
    check_attribute_errors(errors, choice_attribute, "value")

    # make the action valid and to try to send the function for review again
    action.attributes = valid_attributes
    action.save(update_fields=("attributes",))
    response = super_user_api_client.patch(
        get_function_detail_url(function), data={"state": Function.SENT_FOR_REVIEW}
    )
    assert response.status_code == 400
    errors = response.data

    # check that the action is valid and the record errors are still there
    action_errors = errors["phases"][0]["actions"][0]
    assert "attributes" not in action_errors
    record_errors = action_errors["records"][0]
    check_attribute_errors(record_errors, free_text_attribute, "required")
    check_attribute_errors(record_errors, choice_attribute, "value")

    # make the record valid and try to send the function for review again
    record.attributes = valid_attributes
    record.save(update_fields=("attributes",))
    response = super_user_api_client.patch(
        get_function_detail_url(function), data={"state": Function.SENT_FOR_REVIEW}
    )
    assert response.status_code == 400
    errors = response.data

    # the action and the record are valid, there should be only phase errors
    phase_errors = errors["phases"][0]
    check_attribute_errors(phase_errors, free_text_attribute, "required")
    assert "actions" not in phase_errors

    # check supposed valid case as well
    phase.attributes = valid_attributes
    phase.save(update_fields=("attributes",))
    function.attributes = valid_attributes
    function.save(update_fields=("attributes",))
    response = super_user_api_client.patch(
        get_function_detail_url(function), data={"state": Function.SENT_FOR_REVIEW}
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_conditionally_required_attribute_not_allowed_when_not_required(
    monkeypatch,
    super_user_api_client,
    function,
    choice_attribute,
    choice_value_1,
    choice_attribute_2,
    choice_value_2_1,
    choice_value_2_2,
):
    monkeypatch.setitem(
        Function._attribute_validations, "allowed", [choice_attribute.identifier]
    )
    monkeypatch.setitem(
        Function._attribute_validations,
        "conditionally_required",
        {
            choice_attribute.identifier: {
                choice_attribute_2.identifier: choice_value_2_2.value
            }
        },
    )

    function.attributes = {
        choice_attribute.identifier: choice_value_1.value,
        choice_attribute_2.identifier: choice_value_2_1.value,
    }
    function.save(update_fields=("attributes",))

    response = super_user_api_client.patch(
        get_function_detail_url(function), data={"state": Function.SENT_FOR_REVIEW}
    )
    assert response.status_code == 400
    errors = response.data

    check_attribute_errors(errors, choice_attribute, "allowed")


@pytest.mark.django_db
def test_conditionally_required_attribute_multiple_options(
    monkeypatch,
    super_user_api_client,
    function,
    choice_attribute,
    choice_value_1,
    choice_attribute_2,
    choice_value_2_1,
    choice_value_2_2,
):
    monkeypatch.setitem(
        Function._attribute_validations,
        "allowed",
        [choice_attribute.identifier, choice_attribute_2.identifier],
    )
    monkeypatch.setitem(
        Function._attribute_validations,
        "conditionally_required",
        {
            choice_attribute.identifier: {
                choice_attribute_2.identifier: (
                    choice_value_2_1.value,
                    choice_value_2_2.value,
                )
            }
        },
    )

    function.attributes = {choice_attribute_2.identifier: choice_value_2_2.value}
    function.save(update_fields=("attributes",))

    response = super_user_api_client.patch(
        get_function_detail_url(function), data={"state": Function.SENT_FOR_REVIEW}
    )
    errors = response.data
    check_attribute_errors(errors, choice_attribute, "required")


@pytest.mark.django_db
def test_conditionally_disallowed_attributes_normal_situation(
    monkeypatch,
    super_user_api_client,
    function,
    choice_attribute,
    choice_value_1,
    choice_attribute_2,
    choice_value_2_1,
    choice_value_2_2,
):
    monkeypatch.setitem(
        Function._attribute_validations,
        "allowed",
        [choice_attribute.identifier, choice_attribute_2.identifier],
    )
    monkeypatch.setitem(
        Function._attribute_validations,
        "required",
        [choice_attribute.identifier, choice_attribute_2.identifier],
    )
    monkeypatch.setitem(
        Function._attribute_validations,
        "conditionally_disallowed",
        {
            choice_attribute.identifier: {
                choice_attribute_2.identifier: choice_value_2_2.value
            }
        },
    )

    function.attributes = {
        choice_attribute.identifier: choice_value_1.value,
        choice_attribute_2.identifier: choice_value_2_1.value,
    }
    function.save(update_fields=("attributes",))

    response = super_user_api_client.patch(
        get_function_detail_url(function), data={"state": Function.SENT_FOR_REVIEW}
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_conditionally_disallowed_attributes_are_not_required_when_disallowed(
    monkeypatch,
    super_user_api_client,
    function,
    choice_attribute,
    choice_value_1,
    choice_attribute_2,
    choice_value_2_1,
    choice_value_2_2,
):
    monkeypatch.setitem(
        Function._attribute_validations,
        "allowed",
        [choice_attribute.identifier, choice_attribute_2.identifier],
    )
    monkeypatch.setitem(
        Function._attribute_validations,
        "required",
        [choice_attribute.identifier, choice_attribute_2.identifier],
    )
    monkeypatch.setitem(
        Function._attribute_validations,
        "conditionally_disallowed",
        {
            choice_attribute.identifier: {
                choice_attribute_2.identifier: choice_value_2_2.value
            }
        },
    )

    function.attributes = {choice_attribute_2.identifier: choice_value_2_2.value}
    function.save(update_fields=("attributes",))

    response = super_user_api_client.patch(
        get_function_detail_url(function), data={"state": Function.SENT_FOR_REVIEW}
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_conditionally_disallowed_attributes_are_not_required_when_disallowed_multiple_options(
    monkeypatch,
    super_user_api_client,
    function,
    choice_attribute,
    choice_value_1,
    choice_attribute_2,
    choice_value_2_1,
    choice_value_2_2,
):
    monkeypatch.setitem(
        Function._attribute_validations,
        "allowed",
        [choice_attribute.identifier, choice_attribute_2.identifier],
    )
    monkeypatch.setitem(
        Function._attribute_validations,
        "required",
        [choice_attribute.identifier, choice_attribute_2.identifier],
    )
    monkeypatch.setitem(
        Function._attribute_validations,
        "conditionally_disallowed",
        {
            choice_attribute.identifier: {
                choice_attribute_2.identifier: (
                    choice_value_2_1.value,
                    choice_value_2_2.value,
                )
            }
        },
    )

    function.attributes = {choice_attribute_2.identifier: choice_value_2_2.value}
    function.save(update_fields=("attributes",))

    response = super_user_api_client.patch(
        get_function_detail_url(function), data={"state": Function.SENT_FOR_REVIEW}
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_conditionally_disallowed_attributes_errors(
    monkeypatch,
    super_user_api_client,
    function,
    choice_attribute,
    choice_value_1,
    choice_attribute_2,
    choice_value_2_1,
    choice_value_2_2,
):
    monkeypatch.setitem(
        Function._attribute_validations,
        "allowed",
        [choice_attribute.identifier, choice_attribute_2.identifier],
    )
    monkeypatch.setitem(
        Function._attribute_validations,
        "required",
        [choice_attribute.identifier, choice_attribute_2.identifier],
    )
    monkeypatch.setitem(
        Function._attribute_validations,
        "conditionally_disallowed",
        {
            choice_attribute.identifier: {
                choice_attribute_2.identifier: choice_value_2_2.value
            }
        },
    )

    function.attributes = {
        choice_attribute.identifier: choice_value_1.value,
        choice_attribute_2.identifier: choice_value_2_2.value,
    }
    function.save(update_fields=("attributes",))

    response = super_user_api_client.patch(
        get_function_detail_url(function), data={"state": Function.SENT_FOR_REVIEW}
    )
    assert response.status_code == 400
    errors = response.data

    check_attribute_errors(errors, choice_attribute, "allowed")

    function.attributes = {choice_attribute_2.identifier: choice_value_2_1.value}
    function.save(update_fields=("attributes",))

    response = super_user_api_client.patch(
        get_function_detail_url(function), data={"state": Function.SENT_FOR_REVIEW}
    )
    assert response.status_code == 400
    errors = response.data

    check_attribute_errors(errors, choice_attribute, "required")


@pytest.mark.django_db
def test_all_or_none_validation(
    monkeypatch,
    super_user_api_client,
    function,
    choice_attribute,
    choice_attribute_2,
    choice_value_1,
):
    monkeypatch.setitem(
        Function._attribute_validations,
        "allowed",
        (choice_attribute.identifier, choice_attribute_2.identifier),
    )
    monkeypatch.setitem(
        Function._attribute_validations,
        "all_or_none",
        ((choice_attribute.identifier, choice_attribute_2.identifier),),
    )

    function.attributes = {
        choice_attribute.identifier: choice_value_1.value,
    }
    function.save(update_fields=("attributes",))

    response = super_user_api_client.patch(
        get_function_detail_url(function), data={"state": Function.SENT_FOR_REVIEW}
    )
    assert response.status_code == 400
    errors = response.data
    check_attribute_errors(errors, choice_attribute_2, "required")


@pytest.mark.django_db
def test_allow_values_outside_choices_validation(
    monkeypatch,
    super_user_api_client,
    function,
    choice_attribute,
    choice_attribute_2,
    choice_value_1,
    choice_value_2_1,
):
    monkeypatch.setitem(
        Function._attribute_validations,
        "allowed",
        (choice_attribute.identifier, choice_attribute_2.identifier),
    )

    monkeypatch.setitem(
        Function._attribute_validations, "multivalued", (choice_attribute_2.identifier,)
    )

    function.attributes = {
        choice_attribute.identifier: "foo",
        choice_attribute_2.identifier: [choice_value_2_1.value, "bar"],
    }
    function.save(update_fields=("attributes",))

    response = super_user_api_client.patch(
        get_function_detail_url(function), data={"state": Function.SENT_FOR_REVIEW}
    )
    assert response.status_code == 400
    errors = response.data
    check_attribute_errors(errors, choice_attribute, "Invalid value")
    check_attribute_errors(errors, choice_attribute_2, "Invalid value")

    monkeypatch.setitem(
        Function._attribute_validations,
        "allow_values_outside_choices",
        (choice_attribute.identifier, choice_attribute_2.identifier),
    )

    response = super_user_api_client.patch(
        get_function_detail_url(function), data={"state": Function.SENT_FOR_REVIEW}
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_function_patch_required_fields(put_function_data, user_api_client, function):
    set_permissions(user_api_client, Function.CAN_REVIEW)

    function.state = Function.SENT_FOR_REVIEW
    function.save(update_fields=("state",))

    response = user_api_client.patch(
        get_function_detail_url(function), data=put_function_data
    )
    assert response.status_code == 400
    assert '"state", "valid_from" or "valid_to" required.' in str(response.data)


@pytest.mark.parametrize(
    "changes",
    (
        {"valid_from": "2015-01-01"},
        {"valid_to": "2015-01-02"},
        {"valid_from": "2015-01-01", "valid_to": "2015-01-02"},
        {"state": Function.SENT_FOR_REVIEW},
        {"state": Function.SENT_FOR_REVIEW, "valid_to": "2015-01-02"},
        {
            "valid_from": "2015-01-01",
            "valid_to": "2015-01-02",
            "state": Function.SENT_FOR_REVIEW,
        },
    ),
)
@pytest.mark.django_db
def test_function_patching(user_api_client, function, changes):
    set_permissions(user_api_client, Function.CAN_EDIT)
    function.valid_from = "2015-01-01"
    function.save(update_fields=("valid_from",))

    old_data = {field: getattr(function, field) for field in PATCH_FIELDS}

    response = user_api_client.patch(get_function_detail_url(function), data=changes)
    assert response.status_code == 200
    function.refresh_from_db()

    for field in PATCH_FIELDS:
        new_value = getattr(function, field)
        if new_value:
            new_value = str(new_value)

        if field in changes:
            assert new_value == changes[field]
        else:
            assert new_value == old_data[field]


@pytest.mark.django_db
def test_function_validation_date_validation_on_create(
    user_api_client, post_function_data
):
    set_permissions(user_api_client, Function.CAN_EDIT)
    post_function_data["valid_from"] = "2015-01-02"
    post_function_data["valid_to"] = "2015-01-01"

    response = user_api_client.post(FUNCTION_LIST_URL, data=post_function_data)
    assert response.status_code == 400
    assert '"valid_from" cannot be after "valid_to".' in str(response.data)


@pytest.mark.django_db
def test_function_validation_date_validation_on_edit(
    user_api_client, function, put_function_data
):
    url = get_function_detail_url(function)
    set_permissions(user_api_client, (Function.CAN_EDIT, Function.CAN_REVIEW))
    put_function_data["valid_from"] = "2015-01-02"
    put_function_data["valid_to"] = "2015-01-01"

    response = user_api_client.put(url, data=put_function_data)
    assert response.status_code == 400
    assert '"valid_from" cannot be after "valid_to".' in str(response.data)

    response = user_api_client.patch(url, data=put_function_data)
    assert response.status_code == 400
    assert '"valid_from" cannot be after "valid_to".' in str(response.data)


@pytest.mark.parametrize(
    "filtering, expected_indexes, valid",
    (
        ("", [0, 1, 2, 3, 4], True),
        ("valid_at=34234xyz", [], False),
        ("valid_at=1999-05-05", [4], True),
        ("valid_at=2000-05-05", [1, 4], True),
        ("valid_at=2004-05-05", [1, 2, 3, 4], True),
        ("valid_at=2007-05-05", [1], True),
    ),
)
@pytest.mark.django_db
def test_function_validation_date_filtering(
    user_api_client, filtering, expected_indexes, valid
):
    classifications = [
        Classification.objects.get_or_create(code=code)[0]
        for code in ("00", "01", "02", "03", "04")
    ]
    functions = (
        Function.objects.create(classification=classifications[0]),
        Function.objects.create(
            classification=classifications[1], valid_from="2000-05-05"
        ),
        Function.objects.create(
            classification=classifications[2],
            valid_from="2002-05-05",
            valid_to="2004-05-05",
        ),
        Function.objects.create(
            classification=classifications[3],
            valid_from="2003-05-05",
            valid_to="2005-05-05",
        ),
        Function.objects.create(
            classification=classifications[4], valid_to="2006-05-05"
        ),
    )

    response = user_api_client.get(FUNCTION_LIST_URL + "?" + filtering)
    if valid:
        assert response.status_code == 200
        assert_response_functions(
            response, [functions[index] for index in expected_indexes]
        )
    else:
        assert response.status_code == 400
        assert json.loads(response.content) == {"valid_at": ["Enter a valid date."]}


@pytest.mark.parametrize(
    "filtering, expected_indexes, valid",
    (
        ("", [0, 1, 2, 3, 4], True),
        ("modified_at__lt=34234xyz", [], False),
        ("modified_at__lt=1999-05-05 00:00:00", [0], True),
        ("modified_at__lt=2000-05-05 00:00:00", [0], True),
        ("modified_at__lt=2001-05-05 13:00:00", [0, 1], True),
        ("modified_at__lt=2004-05-05 00:00:00", [0, 1, 2, 3], True),
        ("modified_at__lt=2007-05-05 00:00:00", [0, 1, 2, 3, 4], True),
        ("modified_at__gt=34234xyz", [], False),
        ("modified_at__gt=1999-05-05 00:00:00", [1, 2, 3, 4], True),
        ("modified_at__gt=2000-05-05 00:00:00", [1, 2, 3, 4], True),
        ("modified_at__gt=2001-05-05 13:00:00", [2, 3, 4], True),
        ("modified_at__gt=2004-05-05 00:00:00", [4], True),
        ("modified_at__gt=2007-05-05 00:00:00", [], True),
        (
            "modified_at__gt=1970-01-01 00:00:00&modified_at__lt=1971-05-05 00:00:00",
            [0],
            True,
        ),
        (
            "modified_at__gt=2000-05-05 00:00:00&modified_at__lt=2000-05-05 00:00:00",
            [],
            True,
        ),
        (
            "modified_at__gt=2010-05-05 00:00:00&modified_at__lt=2000-05-05 00:00:00",
            [],
            True,
        ),
        (
            "modified_at__gt=2002-05-05 00:00:00&modified_at__lt=2004-05-05 00:00:00",
            [2, 3],
            True,
        ),
        (
            "modified_at__gt=1970-05-05 00:00:00&modified_at__lt=2010-05-05 00:00:00",
            [1, 2, 3, 4],
            True,
        ),
    ),
)
@pytest.mark.django_db
def test_function_validation_modified_at_filtering(
    user_api_client, filtering, expected_indexes, valid
):
    classifications = [
        Classification.objects.get_or_create(code=code)[0]
        for code in ("00", "01", "02", "03", "04")
    ]
    modified_at_values = [
        pytz.utc.localize(
            datetime.datetime(year=1970, month=1, day=1, hour=12, minute=0, second=0)
        ),
        pytz.utc.localize(
            datetime.datetime(year=2000, month=5, day=5, hour=12, minute=0, second=0)
        ),
        pytz.utc.localize(
            datetime.datetime(year=2002, month=5, day=5, hour=12, minute=0, second=0)
        ),
        pytz.utc.localize(
            datetime.datetime(year=2003, month=5, day=5, hour=12, minute=0, second=0)
        ),
        pytz.utc.localize(
            datetime.datetime(year=2006, month=5, day=5, hour=12, minute=0, second=0)
        ),
    ]
    functions = []
    for i, modified_at_value in enumerate(modified_at_values):
        function = Function.objects.create(classification=classifications[i])
        Function.objects.filter(pk=function.pk).update(modified_at=modified_at_value)
        functions.append(Function.objects.get(pk=function.pk))

    response = user_api_client.get(FUNCTION_LIST_URL + "?" + filtering)

    if valid:
        assert response.status_code == 200
        assert_response_functions(
            response, [functions[index] for index in expected_indexes]
        )
    else:
        assert response.status_code == 400
        filter = filtering.split("=")[0]
        assert json.loads(response.content) == {filter: ["Enter a valid date/time."]}


@pytest.mark.django_db
def test_name_field(user_api_client, function, phase, action, record):
    url = get_function_detail_url(function)

    response = user_api_client.get(url)
    assert response.status_code == 200
    data = response.data

    # expect name to match TypeSpecifier
    assert data["phases"][0]["name"] == phase.attributes["TypeSpecifier"]
    assert data["phases"][0]["actions"][0]["name"] == action.attributes["TypeSpecifier"]
    assert (
        data["phases"][0]["actions"][0]["records"][0]["name"]
        == record.attributes["TypeSpecifier"]
    )

    phase.attributes = {"PhaseType": "phase_type"}
    action.attributes = {"ActionType": "action_type"}
    record.attributes = {"RecordType": "record_type"}
    phase.save()
    action.save()
    record.save()

    response = user_api_client.get(url)
    assert response.status_code == 200
    data = response.data

    # no TypeSpecifier, expect name to match type
    assert data["phases"][0]["name"] == phase.attributes["PhaseType"]
    assert data["phases"][0]["actions"][0]["name"] == action.attributes["ActionType"]
    assert (
        data["phases"][0]["actions"][0]["records"][0]["name"]
        == record.attributes["RecordType"]
    )


@pytest.mark.parametrize("endpoint", ("list", "detail"))
@pytest.mark.django_db
def test_attribute_endpoints(
    user_api_client, choice_attribute, choice_value_1, attribute_group, endpoint
):
    url = (
        ATTRIBUTE_LIST_URL
        if endpoint == "list"
        else get_attribute_detail_url(choice_attribute)
    )

    response = user_api_client.get(url)
    assert response.status_code == 200

    if endpoint == "list":
        results = response.data["results"]
        assert len(results) == 1
        attribute_data = results[0]
    else:
        attribute_data = response.data

    assert attribute_data.keys() == {
        "name",
        "values",
        "id",
        "created_at",
        "modified_at",
        "help_text",
        "group",
        "identifier",
        "index",
    }
    assert attribute_data["name"] == choice_attribute.name
    assert attribute_data["identifier"] == choice_attribute.identifier
    assert attribute_data["help_text"] == choice_attribute.help_text
    assert attribute_data["group"] == attribute_group.name
    assert len(attribute_data["values"]) == 1

    value_data = attribute_data["values"][0]
    assert value_data.keys() == {
        "id",
        "value",
        "created_at",
        "modified_at",
        "index",
        "name",
        "help_text",
    }
    assert value_data["value"] == choice_value_1.value


@pytest.mark.django_db
def test_classification_function_field(
    user_api_client, classification, classification_2
):
    function = Function.objects.create(classification=classification)
    Function.objects.create(classification=classification)
    Function.objects.create(classification=classification_2)
    classification_3 = Classification.objects.create(code="05")

    response = user_api_client.get(CLASSIFICATION_LIST_URL)
    assert response.status_code == 200
    assert response.data["results"][0]["function"] == function.uuid.hex
    assert response.data["results"][2]["function"] is None

    response = user_api_client.get(get_classification_detail_url(classification))
    assert response.status_code == 200
    assert response.data["function"] == function.uuid.hex

    response = user_api_client.get(get_classification_detail_url(classification_3))
    assert response.status_code == 200
    assert response.data["function"] is None


def test_include_related(rf):
    request_1 = rf.get("/test/?include_related=true")
    request_2 = rf.get("/test/?include_related=True")
    request_3 = rf.get("/test/?include_related=1")
    request_4 = rf.get("/test/?include_related=foo")
    request_5 = rf.get("/test/")

    assert include_related(request_1)
    assert include_related(request_2)
    assert not include_related(request_3)
    assert not include_related(request_4)
    assert not include_related(request_5)


@pytest.mark.django_db
def test_classification_phase_field(user_api_client, classification, classification_2):
    function = Function.objects.create(classification=classification)
    function_2 = Function.objects.create(classification=classification_2)
    phase = Phase.objects.create(function=function, index=1)
    phase_2 = Phase.objects.create(function=function, index=2)

    response = user_api_client.get(get_classification_detail_url(classification))
    assert response.status_code == 200
    assert response.data["function"] == function.uuid.hex
    assert "phases" not in response.data

    response = user_api_client.get(
        "%s?include_related=True" % get_classification_detail_url(classification)
    )
    assert response.status_code == 200
    assert response.data["function"] == function.uuid.hex
    assert response.data["phases"][0]["id"] == phase.uuid.hex
    assert response.data["phases"][1]["id"] == phase_2.uuid.hex

    response = user_api_client.get(
        "%s?include_related=true" % get_classification_detail_url(classification_2)
    )
    assert response.status_code == 200
    assert response.data["function"] == function_2.uuid.hex
    assert response.data["phases"] == []


@pytest.mark.django_db
def test_function_version_history_field(user_api_client, classification, user_2):
    functions = (
        Function.objects.create(classification=classification, modified_by=None),
        Function.objects.create(
            classification=classification, modified_by=user_api_client.user
        ),
        Function.objects.create(
            classification=classification,
            state=Function.SENT_FOR_REVIEW,
            modified_by=user_2,
        ),
    )

    Function.objects.filter(id=functions[2].id).update(
        state=Function.SENT_FOR_REVIEW, modified_by=user_2
    )
    functions[2].create_metadata_version()

    response = user_api_client.get(FUNCTION_LIST_URL)
    assert response.status_code == 200
    assert "version_history" not in response.data["results"][0]

    response = user_api_client.get(get_function_detail_url(functions[2]))
    assert response.status_code == 200
    version_history = response.data["version_history"]

    assert len(version_history) == 3

    first_version = version_history[0]
    assert first_version.get("modified_at")
    assert first_version["state"] == "draft"
    assert first_version["version"] == 1
    assert "modified_by" not in version_history[0]

    last_version = version_history[2]
    assert last_version["state"] == "sent_for_review"
    assert last_version["version"] == 3

    set_permissions(user_api_client, Function.CAN_VIEW_MODIFIED_BY)

    response = user_api_client.get(get_function_detail_url(functions[2]))
    assert response.status_code == 200
    version_history = response.data["version_history"]

    first_version = version_history[0]
    assert first_version["modified_by"] is None

    middle_version = version_history[1]
    assert middle_version["modified_by"] == "John Rambo"

    last_version = version_history[2]
    assert last_version["modified_by"] == "Rocky Balboa"


@pytest.mark.django_db
def test_classification_version_history(user_api_client, classification):
    classification.pk = None
    classification.state = Classification.SENT_FOR_REVIEW
    classification.valid_from = datetime.datetime.now()
    classification.valid_to = datetime.datetime.now()
    classification.save()

    response = user_api_client.get(get_classification_detail_url(classification))
    assert response.status_code == 200
    version_history = response.data["version_history"]

    assert len(version_history) == 2

    first_version = version_history[0]
    assert first_version.get("modified_at")
    assert first_version["state"] == Classification.APPROVED
    assert first_version["version"] == 1
    assert "modified_by" not in version_history[0]

    last_version = version_history[1]
    assert last_version["state"] == Classification.SENT_FOR_REVIEW
    assert isinstance(last_version["valid_to"], datetime.date)
    assert isinstance(last_version["valid_from"], datetime.date)
    assert last_version["version"] == 2


@pytest.mark.django_db
def test_classification_function_state_field(
    user_api_client, classification, classification_2
):
    Function.objects.create(classification=classification, state=Function.DRAFT)
    Function.objects.create(
        classification=classification, state=Function.SENT_FOR_REVIEW
    )
    Function.objects.create(
        classification=classification_2, state=Function.WAITING_FOR_APPROVAL
    )
    classification_3 = Classification.objects.create(code="05")

    response = user_api_client.get(CLASSIFICATION_LIST_URL)
    assert response.status_code == 200
    assert response.data["results"][0]["function_state"] == Function.SENT_FOR_REVIEW
    assert response.data["results"][2]["function_state"] is None

    response = user_api_client.get(get_classification_detail_url(classification))
    assert response.status_code == 200

    response = user_api_client.get(get_classification_detail_url(classification_3))
    assert response.status_code == 200
    assert response.data["function_state"] is None


@pytest.mark.django_db
def test_classification_function_version_fields(
    user_api_client, classification, classification_2
):
    Function.objects.create(classification=classification)
    Function.objects.create(classification=classification)
    Function.objects.create(classification=classification_2)
    classification_3 = Classification.objects.create(code="05")

    response = user_api_client.get(CLASSIFICATION_LIST_URL)
    assert response.status_code == 200
    assert response.data["results"][0]["function_version"] == 2
    assert response.data["results"][1]["function_version"] == 1
    assert not response.data["results"][2]["function_version"]

    response = user_api_client.get(get_classification_detail_url(classification))
    assert response.status_code == 200
    assert response.data["function_version"] == 2

    response = user_api_client.get(get_classification_detail_url(classification_3))
    assert response.status_code == 200
    assert not response.data["function_version"]


@pytest.mark.django_db
def test_classification_function_validity_date_fields(
    user_api_client, classification, classification_2
):
    Function.objects.create(
        classification=classification,
        valid_from=datetime.date(2019, 1, 1),
        valid_to=datetime.date(2019, 4, 1),
    )
    Function.objects.create(
        classification=classification,
        valid_from=datetime.date(2019, 1, 2),
        valid_to=datetime.date(2019, 4, 2),
    )
    Function.objects.create(
        classification=classification_2,
        valid_from=datetime.date(2019, 1, 3),
        valid_to=datetime.date(2019, 4, 3),
    )
    classification_3 = Classification.objects.create(code="05")

    response = user_api_client.get(CLASSIFICATION_LIST_URL)
    assert response.status_code == 200
    assert response.data["results"][0]["function_valid_from"] == datetime.date(
        2019, 1, 2
    )
    assert response.data["results"][0]["function_valid_to"] == datetime.date(2019, 4, 2)
    assert response.data["results"][1]["function_valid_from"] == datetime.date(
        2019, 1, 3
    )
    assert response.data["results"][1]["function_valid_to"] == datetime.date(2019, 4, 3)
    assert not response.data["results"][2]["function_valid_from"]
    assert not response.data["results"][2]["function_valid_to"]

    response = user_api_client.get(get_classification_detail_url(classification))
    assert response.status_code == 200
    assert response.data["function_valid_from"] == datetime.date(2019, 1, 2)
    assert response.data["function_valid_to"] == datetime.date(2019, 4, 2)

    response = user_api_client.get(get_classification_detail_url(classification_3))
    assert response.status_code == 200
    assert not response.data["function_valid_from"]
    assert not response.data["function_valid_to"]


@pytest.mark.parametrize("authenticated", (False, True))
@pytest.mark.django_db
def test_function_not_exist(api_client, user_api_client, authenticated):
    client = user_api_client if authenticated else api_client

    mock_function = mock.Mock(spec=Function)
    mock_function.uuid = "41418bd7-8cf8-443c-9bdf-8837bde2e73a"

    response = client.get(get_function_detail_url(mock_function))

    assert response.status_code == 404


@pytest.mark.parametrize("authenticated", (False, True))
@pytest.mark.django_db
def test_function_invalid_uuid(api_client, user_api_client, authenticated):
    client = user_api_client if authenticated else api_client

    mock_function = mock.Mock(spec=Function)
    mock_function.uuid = "does-not-exist"

    response = client.get(get_function_detail_url(mock_function))

    assert response.status_code == 400


@pytest.mark.parametrize("authenticated", (False, True))
@pytest.mark.django_db
def test_function_visibility_in_list(
    api_client, user_api_client, classification, classification_2, authenticated
):
    client = user_api_client if authenticated else api_client

    Function.objects.create(classification=classification, state=Function.DRAFT)
    Function.objects.create(classification=classification_2, state=Function.APPROVED)

    response = client.get(FUNCTION_LIST_URL)
    assert response.status_code == 200

    results = response.data["results"]

    if authenticated:
        assert len(results) == 2
    else:
        assert len(results) == 1


@pytest.mark.parametrize("authenticated", (False, True))
@pytest.mark.parametrize("version", ("", 1))
@pytest.mark.django_db
def test_function_visibility_in_list_with_version(
    api_client,
    user_api_client,
    classification,
    classification_2,
    authenticated,
    version,
):
    client = user_api_client if authenticated else api_client

    Function.objects.create(classification=classification, state=Function.APPROVED)
    Function.objects.create(classification=classification_2, state=Function.DRAFT)
    Function.objects.create(classification=classification_2, state=Function.APPROVED)
    Function.objects.create(
        classification=Classification.objects.create(code="05"),
        state=Function.SENT_FOR_REVIEW,
    )

    response = client.get(FUNCTION_LIST_URL + f"?version={version}")
    assert response.status_code == 200

    results = response.data["results"]

    if version == 1:
        if authenticated:
            assert len(results) == 2
        else:
            assert len(results) == 1
    else:
        if authenticated:
            assert len(results) == 3
        else:
            assert len(results) == 2


@pytest.mark.parametrize("authenticated", (False, True))
@pytest.mark.django_db
def test_function_visibility(
    api_client, user_api_client, classification, authenticated
):
    client = user_api_client if authenticated else api_client

    function = Function.objects.create(
        classification=classification, state=Function.DRAFT
    )
    Function.objects.create(
        classification=classification, state=Function.SENT_FOR_REVIEW
    )
    Function.objects.create(
        classification=classification, state=Function.WAITING_FOR_APPROVAL
    )

    response = client.get(FUNCTION_LIST_URL)
    assert response.status_code == 200
    results = response.data["results"]

    if authenticated:
        assert results
    else:
        assert not results

    response = client.get(get_function_detail_url(function))

    if authenticated:
        assert response.status_code == 200
        assert response.data["state"] == Function.WAITING_FOR_APPROVAL
    else:
        assert response.status_code == 401

    Function.objects.create(classification=classification, state=Function.APPROVED)
    Function.objects.create(classification=classification, state=Function.DRAFT)

    response = client.get(FUNCTION_LIST_URL)
    assert response.status_code == 200
    results = response.data["results"]
    assert len(results) == 1

    if authenticated:
        assert results[0]["state"] == Function.DRAFT
    else:
        assert results[0]["state"] == Function.APPROVED

    response = client.get(get_function_detail_url(function))
    assert response.status_code == 200

    if authenticated:
        assert response.data["state"] == Function.DRAFT
    else:
        assert response.data["state"] == Function.APPROVED


@pytest.mark.parametrize("authenticated", (False, True))
@pytest.mark.django_db
def test_function_visibility_in_classification(
    api_client, user_api_client, classification, authenticated
):
    client = user_api_client if authenticated else api_client

    function = Function.objects.create(
        classification=classification, state=Function.DRAFT
    )
    Function.objects.create(
        classification=classification, state=Function.SENT_FOR_REVIEW
    )
    Function.objects.create(
        classification=classification, state=Function.WAITING_FOR_APPROVAL
    )

    response = client.get(CLASSIFICATION_LIST_URL)
    assert response.status_code == 200

    if authenticated:
        assert response.data["results"][0]["function"] == function.uuid.hex
    else:
        assert response.data["results"][0]["function"] is None

    response = client.get(get_classification_detail_url(classification))
    assert response.status_code == 200

    if authenticated:
        assert response.data["function"] == function.uuid.hex
    else:
        assert response.data["function"] is None

    Function.objects.create(classification=classification, state=Function.APPROVED)
    Function.objects.create(classification=classification, state=Function.DRAFT)
    Function.objects.create(classification=classification, state=Function.APPROVED)

    response = client.get(CLASSIFICATION_LIST_URL)
    assert response.status_code == 200
    assert response.data["results"][0]["function"] == function.uuid.hex

    response = client.get(get_classification_detail_url(classification))
    assert response.status_code == 200
    assert response.data["function"] == function.uuid.hex


@pytest.mark.parametrize("authenticated", (False, True))
@pytest.mark.parametrize("index", (0, 1, 2, 3, 4, 5))
@pytest.mark.django_db
def test_function_version_filter(
    api_client, user_api_client, classification, authenticated, index
):
    client = user_api_client if authenticated else api_client

    functions = [
        Function.objects.create(classification=classification, state=Function.APPROVED),
        Function.objects.create(classification=classification, state=Function.DRAFT),
        Function.objects.create(classification=classification, state=Function.APPROVED),
        Function.objects.create(classification=classification, state=Function.DRAFT),
        Function.objects.create(
            classification=classification, state=Function.SENT_FOR_REVIEW
        ),
        Function.objects.create(
            classification=classification, state=Function.WAITING_FOR_APPROVAL
        ),
    ]

    function = functions[index]
    response = client.get(
        get_function_detail_url(function) + "?version={}".format(index + 1)
    )

    if index == 1:
        # Drafts leading to new approved version will be deleted after approved version is saved.
        assert response.status_code == 404
    elif authenticated or function.state == Function.APPROVED:
        assert response.status_code == 200
        assert response.data["state"] == function.state
    else:
        assert response.status_code == 401


@pytest.mark.django_db
def test_function_classification_code_filtering(
    api_client, classification, classification_2
):
    Function.objects.create(classification=classification, state=Function.APPROVED)
    Function.objects.create(classification=classification_2, state=Function.APPROVED)

    list_response = api_client.get(FUNCTION_LIST_URL)
    list_results = list_response.data["results"]
    response = api_client.get(
        FUNCTION_LIST_URL + "?classification_code=" + classification.code
    )
    results = response.data["results"]

    assert list_response.status_code == 200
    assert len(list_results) == 2
    assert list_results[0]["classification_code"] == classification.code
    assert list_results[1]["classification_code"] == classification_2.code

    assert response.status_code == 200
    assert len(results) == 1
    assert list_results[0]["classification_code"] == classification.code


@pytest.mark.django_db
def test_function_information_system_filtering(api_client, classification):
    function = Function.objects.create(
        classification=classification, state=Function.APPROVED
    )
    function_2 = Function.objects.create(
        classification=classification, state=Function.APPROVED
    )
    function_3 = Function.objects.create(
        classification=classification, state=Function.APPROVED
    )

    phase = Phase.objects.create(
        attributes={"TypeSpecifier": "test phase"}, function=function, index=1
    )
    phase_2 = Phase.objects.create(
        attributes={"TypeSpecifier": "test phase"}, function=function_2, index=1
    )
    phase_3 = Phase.objects.create(
        attributes={"TypeSpecifier": "test phase"}, function=function_3, index=1
    )

    action = Action.objects.create(
        attributes={"TypeSpecifier": "test action"}, phase=phase, index=1
    )
    action_2 = Action.objects.create(
        attributes={"TypeSpecifier": "test action"}, phase=phase_2, index=1
    )
    action_3 = Action.objects.create(
        attributes={"TypeSpecifier": "test action"}, phase=phase_3, index=1
    )

    Record.objects.create(
        attributes={"InformationSystem": "xyz"}, action=action, index=1
    )
    Record.objects.create(
        attributes={"InformationSystem": "123"}, action=action_2, index=1
    )
    Record.objects.create(
        attributes={"NotAnInformationSystem": "xyz"}, action=action_3, index=1
    )

    response = api_client.get(FUNCTION_LIST_URL + "?information_system=xyz")
    assert response.status_code == 200
    results = response.data["results"]
    assert len(results) == 1
    assert results[0]["id"] == function.uuid.hex


@pytest.mark.parametrize("authenticated", (False, True))
@pytest.mark.django_db
def test_function_visibility_in_version_history(
    api_client, user_api_client, classification, authenticated
):
    client = user_api_client if authenticated else api_client

    function = Function.objects.create(
        classification=classification, state=Function.APPROVED
    )
    Function.objects.create(classification=classification, state=Function.DRAFT)
    Function.objects.create(classification=classification, state=Function.APPROVED)
    Function.objects.create(classification=classification, state=Function.DRAFT)
    Function.objects.create(
        classification=classification, state=Function.SENT_FOR_REVIEW
    )
    Function.objects.create(
        classification=classification, state=Function.WAITING_FOR_APPROVAL
    )

    response = client.get(get_function_detail_url(function))
    assert response.status_code == 200

    version_history = response.data["version_history"]
    version_history_states = [vh["state"] for vh in version_history]

    if authenticated:
        # The drafts leading up to a approved version will be deleted. Only drafts that don't have
        # later approved version are not deleted automatically.
        assert version_history_states == [
            Function.APPROVED,
            Function.APPROVED,
            Function.DRAFT,
            Function.SENT_FOR_REVIEW,
            Function.WAITING_FOR_APPROVAL,
        ]
    else:
        assert version_history_states == [Function.APPROVED, Function.APPROVED]
        assert version_history[0]["version"] == 1
        assert version_history[1]["version"] == 3


@pytest.mark.django_db
def test_function_delete_on_approve(user_api_client, classification):
    function = Function.objects.create(
        classification=classification, state=Function.DRAFT
    )
    Function.objects.create(
        classification=classification, state=Function.SENT_FOR_REVIEW
    )
    Function.objects.create(
        classification=classification, state=Function.WAITING_FOR_APPROVAL
    )
    Function.objects.create(classification=classification, state=Function.APPROVED)
    Function.objects.create(classification=classification, state=Function.DRAFT)
    Function.objects.create(classification=classification, state=Function.APPROVED)
    Function.objects.create(classification=classification, state=Function.DRAFT)
    Function.objects.create(
        classification=classification, state=Function.SENT_FOR_REVIEW
    )
    Function.objects.create(
        classification=classification, state=Function.WAITING_FOR_APPROVAL
    )

    response = user_api_client.get(get_function_detail_url(function))
    assert response.status_code == 200

    version_history = response.data["version_history"]
    version_history_states = [vh["state"] for vh in version_history]

    assert version_history_states == [
        Function.APPROVED,
        Function.APPROVED,
        Function.DRAFT,
        Function.SENT_FOR_REVIEW,
        Function.WAITING_FOR_APPROVAL,
    ]


@pytest.mark.django_db
def test_function_post_when_not_allowed(post_function_data, user_api_client):
    set_permissions(user_api_client, Function.CAN_EDIT)
    parent_classification = Classification.objects.get(
        uuid=post_function_data["classification"]["id"],
        version=post_function_data["classification"]["version"],
    )
    parent_classification.function_allowed = False
    parent_classification.save(update_fields=("function_allowed",))

    response = user_api_client.post(FUNCTION_LIST_URL, data=post_function_data)
    assert response.status_code == 400
    expected_error = (
        "Classification %s does not allow function creation."
        % parent_classification.uuid.hex
    )
    assert expected_error in response.data["non_field_errors"]


@pytest.mark.django_db
def test_function_post_new_when_existing_function(
    rf, function, phase, action, record, user_api_client, super_user_api_client
):
    set_permissions(user_api_client, Function.CAN_EDIT)
    classification = function.classification
    classification.pk = None
    classification.save()

    function.refresh_from_db()

    function_key = get_bulk_update_function_key(function)
    post_data = {
        "description": "Bulk update description",
        "state": Function.APPROVED,
        "changes": {
            function_key: {
                "attributes": {"TypeSpecifier": "bulk updated test thing"},
            }
        },
    }

    with freezegun.freeze_time("2020-01-01 12:00"):
        response = super_user_api_client.post(BULK_UPDATE_LIST_URL, post_data)

    function.bulk_update = BulkUpdate.objects.first()
    function.save()

    new_classification = Classification.objects.latest_version().get(
        code=function.classification.code
    )
    post_data = {
        "classification": {
            "id": new_classification.uuid.hex,
            "version": new_classification.version,
        }
    }

    response = user_api_client.post(FUNCTION_LIST_URL, data=post_data)

    class View:
        action = "create"

    dummy_request = rf.get(get_function_detail_url(function))
    dummy_request.user = user_api_client.user
    dummy_context = {"view": View(), "request": dummy_request}
    function_data = FunctionTestDetailSerializer(function, context=dummy_context).data
    response_data_json = response.json()
    for attr in ["modified_at", "created_at", "actions", "id"]:
        response_data_json["phases"][0].pop(attr)
        function_data["phases"][0].pop(attr)
    assert response_data_json["phases"][0] == function_data["phases"][0]
    response_data_json.pop("phases")
    function_data.pop("phases")

    new_phase = (
        Function.objects.filter(classification=new_classification)
        .latest_version()
        .first()
        .phases.first()
    )
    assert new_phase.attributes == phase.attributes
    assert new_phase.actions.first().attributes == phase.actions.first().attributes
    assert (
        new_phase.actions.first().records.first().attributes
        == phase.actions.first().records.first().attributes
    )
    assert response_data_json["version"] != function_data["version"]
    assert (
        response_data_json["classification"]["version"]
        != function_data["classification"]["version"]
    )
    for attr in [
        "created_at",
        "modified_at",
        "version",
        "classification",
        "bulk_update",
    ]:
        function_data.pop(attr)
        response_data_json.pop(attr)
    assert response_data_json == function_data


@pytest.mark.parametrize("authenticated", (False, True))
@pytest.mark.django_db
def test_classification_fields_visibility(
    api_client, user_api_client, classification, authenticated
):
    client = user_api_client if authenticated else api_client

    response = client.get(get_classification_detail_url(classification))
    assert response.status_code == 200

    if authenticated:
        assert (
            response.data["description_internal"] == classification.description_internal
        )
        assert (
            response.data["additional_information"]
            == classification.additional_information
        )
    else:
        assert "description_internal" not in response.data
        assert "additional_information" not in response.data


@pytest.mark.parametrize("has_permission", (False, True))
@pytest.mark.django_db
def test_classification_create_requires_permission(
    user_api_client, user_2_api_client, has_permission
):
    set_permissions(user_api_client, Classification.CAN_EDIT)
    client = user_api_client if has_permission else user_2_api_client
    data = {"code": "05", "title": "test classification created through the API"}

    response = client.post(CLASSIFICATION_LIST_URL, data=data)

    if has_permission:
        assert response.status_code == 201
        assert Classification.objects.count() == 1
        classification = Classification.objects.first()
        assert classification.code == data["code"]
        assert classification.title == data["title"]
        assert classification.version == 1
        assert classification.created_by == client.user
        assert classification.modified_by == client.user
    else:
        assert response.status_code == 403
        assert Classification.objects.count() == 0


@pytest.mark.parametrize("has_permission", (False, True))
@pytest.mark.django_db
def test_classification_update_requires_permission(
    user_api_client, user_2_api_client, classification, has_permission
):
    set_permissions(user_api_client, Classification.CAN_EDIT)
    client = user_api_client if has_permission else user_2_api_client
    classification.state = Classification.DRAFT
    classification.save(update_fields=["state"])
    data = {
        "state": Classification.SENT_FOR_REVIEW,
    }

    response = client.patch(get_classification_detail_url(classification), data=data)

    if has_permission:
        assert response.status_code == 200
        assert Classification.objects.count() == 1
        classification.refresh_from_db()
        assert classification.state == Classification.SENT_FOR_REVIEW
        assert classification.modified_by == client.user
    else:
        assert response.status_code == 403
        assert Classification.objects.count() == 1
        classification.refresh_from_db()
        assert classification.state == Classification.DRAFT


@pytest.mark.django_db
def test_classification_patch_does_not_create_new_version(
    user_api_client, classification
):
    set_permissions(user_api_client, Classification.CAN_EDIT)
    classification.state = Classification.DRAFT
    classification.save(update_fields=["state"])
    data = {
        "state": Classification.SENT_FOR_REVIEW,
    }

    assert classification.version == 1
    response = user_api_client.patch(
        get_classification_detail_url(classification), data=data
    )

    assert response.status_code == 200
    assert Classification.objects.count() == 1
    classification.refresh_from_db()
    assert classification.state == Classification.SENT_FOR_REVIEW
    assert classification.version == 1


@pytest.mark.django_db
def test_classification_put_creates_new_version(user_api_client, classification):
    set_permissions(user_api_client, Classification.CAN_EDIT)
    data = {
        "code": classification.code,
        "title": "Updated classification title",
        "description": "Updated classification description",
    }

    response = user_api_client.put(
        get_classification_detail_url(classification), data=data
    )

    assert response.status_code == 200
    assert response.json()["version"] == 2
    assert Classification.objects.count() == 2
    new_version = Classification.objects.latest_version().get(code=classification.code)
    assert new_version.code == classification.code
    assert new_version.uuid == classification.uuid
    assert new_version.version == 2
    assert new_version.title == data["title"]
    assert new_version.description == data["description"]
    assert new_version.state == Classification.DRAFT


@pytest.mark.parametrize(
    "parent_state", (Classification.APPROVED, Classification.DRAFT)
)
@pytest.mark.django_db
def test_classification_put_parent_version_change(
    user_api_client, parent_classification, classification, parent_state
):
    set_permissions(user_api_client, Classification.CAN_EDIT)
    classification.parent = parent_classification
    classification.save(update_fields=["parent"])
    parent_classification_v2 = Classification.objects.create(
        uuid=parent_classification.uuid,
        title="Updated title",
        code=parent_classification.code,
        function_allowed=parent_classification.function_allowed,
        state=parent_state,
    )
    assert parent_classification_v2.version == 2
    assert classification.parent == parent_classification

    data = {
        "code": classification.code,
        "title": "Updated classification title",
        "description": "Updated classification description",
        "parent": {
            "id": parent_classification_v2.uuid.hex,
            "version": parent_classification_v2.version,
        },
    }
    response = user_api_client.put(
        get_classification_detail_url(classification), data=data
    )
    response_data = response.json()

    assert response.status_code == 200
    new_version = Classification.objects.latest_version().get(uuid=classification.uuid)
    assert new_version.version == 2
    assert new_version.parent == parent_classification_v2
    assert response_data["parent"]["id"] == parent_classification_v2.uuid.hex
    assert response_data["parent"]["version"] == parent_classification_v2.version


@pytest.mark.parametrize(
    "old_state,new_state,is_ok",
    (
        (Classification.DRAFT, Classification.SENT_FOR_REVIEW, True),
        (Classification.DRAFT, Classification.WAITING_FOR_APPROVAL, False),
        (Classification.DRAFT, Classification.APPROVED, False),
        (Classification.SENT_FOR_REVIEW, Classification.DRAFT, True),
        (Classification.SENT_FOR_REVIEW, Classification.WAITING_FOR_APPROVAL, True),
        (Classification.SENT_FOR_REVIEW, Classification.APPROVED, False),
        (Classification.WAITING_FOR_APPROVAL, Classification.DRAFT, True),
        (Classification.WAITING_FOR_APPROVAL, Classification.SENT_FOR_REVIEW, False),
        (Classification.WAITING_FOR_APPROVAL, Classification.APPROVED, True),
        (Classification.APPROVED, Classification.DRAFT, True),
        (Classification.APPROVED, Classification.SENT_FOR_REVIEW, False),
        (Classification.APPROVED, Classification.WAITING_FOR_APPROVAL, False),
    ),
)
@pytest.mark.django_db
def test_classification_state_change(
    user_api_client, classification, old_state, new_state, is_ok
):
    set_permissions(
        user_api_client,
        [
            Classification.CAN_EDIT,
            Classification.CAN_REVIEW,
            Classification.CAN_APPROVE,
        ],
    )
    classification.state = old_state
    classification.save(update_fields=["state"])
    data = {"state": new_state, "name": "this should be ignored"}

    response = user_api_client.patch(
        get_classification_detail_url(classification), data=data
    )

    if is_ok:
        assert response.status_code == 200
        assert response.data["version"] == 1
        assert response.data["state"] == new_state

        classification.refresh_from_db()
        assert classification.version == 1
        assert classification.state == new_state
    else:
        assert response.status_code == 400
        assert response.data["state"] == [_("Invalid state change.")]


@pytest.mark.django_db
def test_classification_modified_by(classification, user_api_client, user):
    set_permissions(user_api_client, Classification.CAN_VIEW_MODIFIED_BY)

    response = user_api_client.get(get_classification_detail_url(classification))
    assert response.status_code == 200
    assert response.data["modified_by"] is None

    classification.modified_by = user
    classification.save()

    response = user_api_client.get(get_classification_detail_url(classification))
    assert response.status_code == 200
    assert response.data["modified_by"] == "%s %s" % (user.first_name, user.last_name)


@pytest.mark.django_db
def test_classification_anonymous_cannot_view_modified_by(
    classification, api_client, user
):
    classification.state = Function.APPROVED
    classification.modified_by = user
    classification.save()

    response = api_client.get(get_classification_detail_url(classification))
    assert response.status_code == 200
    assert "modified_by" not in response.data


@pytest.mark.django_db
def test_classification_version_filter(user_api_client, classification):
    classification_v2 = Classification.objects.create(
        uuid=classification.uuid,
        title="test classification v2",
        code=classification.code,
        function_allowed=classification.function_allowed,
    )
    assert classification_v2.version == 2

    response = user_api_client.get(
        get_classification_detail_url(classification), {"version": 2}
    )

    data = response.json()
    assert data["title"] == "test classification v2"


@pytest.mark.django_db
def test_version_history_modified_by(
    user_2_api_client, super_user_api_client, function, classification, user
):
    set_permissions(user_2_api_client, Function.CAN_EDIT)
    Function.objects.create(
        classification=classification, state=Function.DRAFT, modified_by=user
    )
    Function.objects.create(
        classification=classification, state=Function.DRAFT, modified_by=user
    )
    data = {"state": Function.SENT_FOR_REVIEW}

    response = user_2_api_client.patch(get_function_detail_url(function), data=data)
    assert response.status_code == 200

    response = super_user_api_client.get(get_function_detail_url(function))
    assert response.status_code == 200
    version_history = response.data["version_history"]
    assert version_history[0]["modified_by"] is None
    assert version_history[1]["modified_by"] == "John Rambo"
    assert version_history[2]["modified_by"] == "Rocky Balboa"


@pytest.mark.django_db
def test_bulk_update_add_permission(
    user_api_client, user_2_api_client, super_user_api_client
):
    set_permissions(user_2_api_client, BulkUpdate.CAN_ADD)
    request_payload = {
        "description": "Lorem ipsum dolor sit amet",
        "state": "approved",
        "changes": {},
    }
    user_response = user_api_client.post(BULK_UPDATE_LIST_URL, request_payload)
    user_2_response = user_2_api_client.post(BULK_UPDATE_LIST_URL, request_payload)
    super_user_response = super_user_api_client.post(
        BULK_UPDATE_LIST_URL, request_payload
    )

    assert user_response.status_code == 403
    assert user_2_response.status_code == 201
    assert super_user_response.status_code == 201


@pytest.mark.parametrize("permission", (None, "change", "superuser"))
@pytest.mark.django_db
def test_bulk_update_change_permission(bulk_update, user_api_client, permission):
    if permission == "change":
        set_permissions(user_api_client, BulkUpdate.CAN_CHANGE)
    elif permission == "superuser":
        user_api_client.user.is_superuser = True
        user_api_client.user.save(update_fields=["is_superuser"])

    url = get_bulk_update_detail_url(bulk_update)
    response = user_api_client.patch(url, {"changes": {"foo": "bar"}})
    bulk_update.refresh_from_db()

    if not permission:
        assert response.status_code == 403
        assert bulk_update.modified_by is None
    else:
        assert response.status_code == 200
        assert bulk_update.modified_by == user_api_client.user


@pytest.mark.parametrize("permission", (None, "approve", "superuser"))
@pytest.mark.django_db
def test_bulk_update_approve_permission(
    bulk_update, function, user_api_client, permission
):
    if permission == "approve":
        set_permissions(user_api_client, BulkUpdate.CAN_APPROVE)
    elif permission == "superuser":
        user_api_client.user.is_superuser = True
        user_api_client.user.save(update_fields=["is_superuser"])

    function_key = get_bulk_update_function_key(function)
    bulk_update.changes = {
        function_key: {"attributes": {"TypeSpecifier": "bulk updated test thing"}}
    }
    bulk_update.save(update_fields=["changes"])

    url = get_bulk_update_approve_url(bulk_update)
    response = user_api_client.post(url, {})
    bulk_update.refresh_from_db()

    if not permission:
        assert response.status_code == 403
        assert bulk_update.is_approved is False
        assert bulk_update.approved_by is None
    else:
        assert response.status_code == 200
        assert bulk_update.is_approved is True
        assert bulk_update.approved_by == user_api_client.user


@pytest.mark.django_db
def test_bulk_update_create(function, super_user_api_client):
    function_key = get_bulk_update_function_key(function)
    post_data = {
        "description": "Bulk update description",
        "state": Function.APPROVED,
        "changes": {
            function_key: {
                "attributes": {"TypeSpecifier": "bulk updated test thing"},
            }
        },
    }

    with freezegun.freeze_time("2019-04-01 12:00"):
        response = super_user_api_client.post(BULK_UPDATE_LIST_URL, post_data)

    bulk_update = BulkUpdate.objects.first()
    response_content = json.loads(response.content)
    assert response.status_code == 201
    assert response_content["id"] == bulk_update.pk.hex
    assert bulk_update.description == post_data["description"]
    assert bulk_update.state == Function.APPROVED
    assert bulk_update.changes == post_data["changes"]
    assert bulk_update.created_at == datetime.datetime(
        2019, 4, 1, 12, 0, tzinfo=pytz.UTC
    )
    assert bulk_update.modified_at == datetime.datetime(
        2019, 4, 1, 12, 0, tzinfo=pytz.UTC
    )
    assert bulk_update.modified_by == super_user_api_client.user


@pytest.mark.django_db
def test_bulk_update_change(bulk_update, function, super_user_api_client):
    url = get_bulk_update_detail_url(bulk_update)
    function_key = get_bulk_update_function_key(function)
    patch_data = {
        "changes": {
            function_key: {
                "attributes": {"TypeSpecifier": "bulk updated test thing"},
            }
        }
    }
    get_response = super_user_api_client.get(url)
    patch_response = super_user_api_client.patch(url, patch_data)

    get_response_data = json.loads(get_response.content)
    patch_response_data = json.loads(patch_response.content)

    assert get_response_data["id"] == patch_response_data["id"]
    assert get_response_data["description"] == patch_response_data["description"]
    assert get_response_data["created_at"] == patch_response_data["created_at"]
    assert get_response_data["is_approved"] == patch_response_data["is_approved"]
    assert get_response_data["state"] == patch_response_data["state"]

    assert get_response_data["modified_by"] != patch_response_data["modified_by"]
    assert get_response_data["modified_at"] != patch_response_data["modified_at"]
    assert get_response_data["changes"] != patch_response_data["changes"]

    assert patch_response_data["changes"] == patch_data["changes"]
    assert patch_response_data["modified_by"] == "Kurt Sloane"


@pytest.mark.parametrize("permission", (None, "delete", "superuser"))
@pytest.mark.django_db
def test_bulk_update_delete_permission(bulk_update, user_api_client, permission):
    if permission == "delete":
        set_permissions(user_api_client, BulkUpdate.CAN_DELETE)
    elif permission == "superuser":
        user_api_client.user.is_superuser = True
        user_api_client.user.save(update_fields=["is_superuser"])

    response = user_api_client.delete(get_bulk_update_detail_url(bulk_update))

    if not permission:
        assert response.status_code == 403
        assert BulkUpdate.objects.filter(pk=bulk_update.pk).exists()
    else:
        assert response.status_code == 204
        assert not BulkUpdate.objects.filter(pk=bulk_update.pk).exists()


@pytest.mark.parametrize("permission", (None, "view_modified_by", "superuser"))
@pytest.mark.django_db
def test_bulk_update_modified_by_display(bulk_update, user_api_client, permission):
    if permission == "view_modified_by":
        set_permissions(user_api_client, Function.CAN_VIEW_MODIFIED_BY)
    elif permission == "superuser":
        user_api_client.user.is_superuser = True
        user_api_client.user.save(update_fields=["is_superuser"])

    bulk_update.created_by = user_api_client.user
    bulk_update.modified_by = user_api_client.user
    bulk_update.save()

    response = user_api_client.get(get_bulk_update_detail_url(bulk_update))
    response_data = json.loads(response.content.decode("utf-8"))

    if not permission:
        assert "modified_by" not in response_data.keys()
    else:
        assert response_data["modified_by"] == "John Rambo"


@pytest.mark.django_db
def test_record_api_put(record, super_user_api_client):
    data = {
        "attributes": {"TypeSpecifier": "updated record"},
        "index": 123,
    }

    response = super_user_api_client.put(get_record_detail_url(record), data=data)

    record.refresh_from_db()
    assert response.status_code == 405
    assert record.index == 1
    assert record.attributes == {"TypeSpecifier": "test record"}


@pytest.mark.django_db
def test_record_api_patch(record, super_user_api_client):
    data = {
        "attributes": {"TypeSpecifier": "updated record"},
    }

    response = super_user_api_client.patch(get_record_detail_url(record), data=data)

    record.refresh_from_db()
    assert response.status_code == 405
    assert record.index == 1
    assert record.attributes == {"TypeSpecifier": "test record"}


@pytest.mark.django_db
def test_record_api_delete(record, super_user_api_client):
    response = super_user_api_client.delete(get_record_detail_url(record))

    assert response.status_code == 405
    assert Record.objects.filter(pk=record.pk).exists()


@pytest.mark.parametrize("permission", (None, "view_modified_by", "superuser"))
@pytest.mark.django_db
def test_record_modified_by_display(record, user_api_client, permission):
    if permission == "view_modified_by":
        set_permissions(user_api_client, Function.CAN_VIEW_MODIFIED_BY)
    elif permission == "superuser":
        user_api_client.user.is_superuser = True
        user_api_client.user.save(update_fields=["is_superuser"])

    record.created_by = user_api_client.user
    record.modified_by = user_api_client.user
    record.save()

    response = user_api_client.get(get_record_detail_url(record))
    response_data = response.json()

    if not permission:
        assert "modified_by" not in response_data.keys()
    else:
        assert response_data["modified_by"] == "John Rambo"
