import datetime
import uuid
import pytest
import pytz
from rest_framework.reverse import reverse
from metarecord.models import Action, Attribute, Classification, Function, Phase, Record
from metarecord.tests.utils import assert_response_functions, check_attribute_errors, set_permissions

CLASSIFICATION_LIST_URL = reverse('v1:classification-list')
FUNCTION_LIST_URL = reverse('v1:function-list')
ATTRIBUTE_LIST_URL = reverse('v1:attribute-list')


def get_classification_detail_url(classification):
    return reverse('v1:classification-detail', kwargs={'uuid': classification.uuid})


def get_function_detail_url(function):
    return reverse('v1:function-detail', kwargs={'uuid': function.uuid})


def get_attribute_detail_url(attribute):
    return reverse('v1:attribute-detail', kwargs={'pk': attribute.id})


@pytest.fixture
def function_data(function, free_text_attribute, choice_attribute):
    return {
        'name': 'new function',
        'function_id': function.classification.code,
        'parent': 'xyz',
        'attributes': {
            free_text_attribute.identifier: 'new function attribute value',
        },
        'phases': [
            {
                'actions': [
                    {
                        'records': [
                            {
                                'attributes': {
                                    choice_attribute.identifier: 'new record attribute value',
                                },
                            }
                        ]
                    }
                ]
            }
        ]
    }


# by default disable hardcoded attribute validations so that they don't interfere
# in tests unrelated to attribute validation, attribute validations are tested
# explicitly in their own tests.
@pytest.fixture(autouse=True)
def disable_attribute_validations(monkeypatch):
    _attribute_validations = {
        'allowed': None,
        'required': None,
        'conditionally_required': None,
        'multivalued': None,
        'all_or_none': None,
    }

    for structural_element in (Function, Phase, Action, Record):
        monkeypatch.setattr(structural_element, '_attribute_validations', _attribute_validations)


def _check_function_object_matches_data(function_obj, data):
    new_function = function_obj

    assert new_function.attributes == data['attributes']
    assert new_function.phases.count() == 1

    new_phase = new_function.phases.first()
    phase_data = data['phases'][0]
    assert new_phase.attributes == {}
    assert new_phase.actions.count() == 1

    new_action = new_phase.actions.first()
    action_data = phase_data['actions'][0]
    assert new_action.attributes == {}
    assert new_action.records.count() == 1

    new_record = new_action.records.first()
    record_data = action_data['records'][0]
    assert new_record.attributes == record_data['attributes']


@pytest.fixture
def attribute(choice_attribute):
    return choice_attribute


@pytest.mark.parametrize('resource', [
    'function',
    'phase',
    'action',
    'record',
    'attribute',
    'template',
    'classification',
])
@pytest.mark.django_db
def test_get(api_client, resource, function, phase, action, record, attribute, template, classification):
    """
    Test GET to every resource's list and detail endpoint.
    """
    list_url = reverse('v1:%s-list' % resource)
    response = api_client.get(list_url)
    assert response.status_code == 200
    assert len(response.data['results'])

    id_field = 'pk' if resource is 'attribute' else 'uuid'
    id_value = getattr(locals().get(resource), id_field)
    detail_url = reverse('v1:%s-detail' % resource.replace('_', ''), kwargs={id_field: id_value})
    response = api_client.get(detail_url)
    assert response.status_code == 200
    assert response.data


@pytest.mark.django_db
def test_get_attribute_schemas(api_client):
    url = '{}schemas/'.format(reverse('v1:attribute-list'))
    response = api_client.get(url)
    assert response.status_code == 200

    for element in ('function', 'phase', 'action', 'record'):
        assert len(response.data.get(element))


@pytest.mark.django_db
def test_function_versioning(api_client, classification, classification_2):
    first_draft = Function.objects.create(classification=classification, attributes={'subject': 'first draft'})
    first_approved = Function.objects.create(
        classification=classification, state=Function.APPROVED, attributes={'subject': 'first approved'}
    )
    second_approved = Function.objects.create(
        classification=classification, state=Function.APPROVED, attributes={'subject': 'second approved'}
    )
    second_draft = Function.objects.create(classification=classification, attributes={'subject': 'second draft'})
    other_function = Function.objects.create(classification=classification_2, attributes={'subject': 'other function'})
    template = Function.objects.create(is_template=True, attributes={'subject': 'template'})

    assert first_draft.uuid == first_approved.uuid == second_approved.uuid == second_draft.uuid
    assert first_draft.version == 1
    assert first_approved.version == 2
    assert second_approved.version == 3
    assert second_draft.version == 4
    assert other_function.version == 1
    assert template.version is None

    url = reverse('v1:function-detail', kwargs={'uuid': first_draft.uuid})

    # /function/<uuid>/ should return the latest version
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['attributes']['subject'] == 'second draft'

    # /function/<uuid>/?state=approved should return the latest approved version
    response = api_client.get(url + '?state=approved')
    assert response.status_code == 200
    assert response.data['attributes']['subject'] == 'second approved'


@pytest.mark.django_db
def test_unauthenticated_user_cannot_post_or_put_functions(function_data, api_client, function):
    response = api_client.post(FUNCTION_LIST_URL, data=function_data)
    assert response.status_code == 401

    response = api_client.put(get_function_detail_url(function), data=function_data)
    assert response.status_code == 401


@pytest.mark.django_db
def test_cannot_post_functions(user_api_client, function, function_data):
    response = user_api_client.post(FUNCTION_LIST_URL, data=function_data)
    assert response.status_code == 405


@pytest.mark.django_db
def test_function_put(function_data, user_api_client, function, phase, action, record):
    set_permissions(user_api_client, Function.CAN_EDIT)

    models = (function, phase, action, record)
    modified_ats = [obj.modified_at for obj in models]  # store original modified_at timestamps

    response = user_api_client.put(get_function_detail_url(function), data=function_data)
    assert response.status_code == 200

    new_function = Function.objects.last()
    _check_function_object_matches_data(new_function, function_data)

    assert new_function.version == 2
    assert new_function.uuid == function.uuid

    # check that the original objects haven't been modified
    for index, obj in enumerate(models):
        obj.refresh_from_db()
        assert obj.modified_at == modified_ats[index]


@pytest.mark.django_db
def test_function_put_invalid_attributes(function_data, user_api_client, function):
    function_data['function_id'] = function.classification.code
    function_data['attributes'] = {'InvalidFunctionAttribute': 'value'}
    function_data['phases'][0]['attributes'] = {'InvalidPhaseAttribute': 'value'}

    response = user_api_client.put(get_function_detail_url(function), data=function_data)
    assert response.status_code == 400
    assert response.data['attributes']['InvalidFunctionAttribute'] == ['Invalid attribute.']
    assert response.data['phases'][0]['attributes']['InvalidPhaseAttribute'] == ['Invalid attribute.']


@pytest.mark.django_db
def test_function_multivalued_attribute(monkeypatch, function_data, user_api_client, function, free_text_attribute):
    set_permissions(user_api_client, Function.CAN_EDIT)

    monkeypatch.setitem(Function._attribute_validations, 'multivalued', [free_text_attribute.identifier])

    function_data['function_id'] = function.classification.code
    function_data['attributes'] = {
        free_text_attribute.identifier: ['value1', 'value2']
    }

    response = user_api_client.put(get_function_detail_url(function), data=function_data)
    assert response.status_code == 200

    function_data['state'] = Function.SENT_FOR_REVIEW
    response = user_api_client.patch(get_function_detail_url(function), data=function_data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_function_multivalued_attribute_allow_single(monkeypatch, function_data, user_api_client, function,
                                                     free_text_attribute):
    set_permissions(user_api_client, Function.CAN_EDIT)

    monkeypatch.setitem(Function._attribute_validations, 'multivalued', [free_text_attribute.identifier])

    function_data['function_id'] = function.classification.code
    function_data['attributes'] = {
        free_text_attribute.identifier: 'value1'
    }

    response = user_api_client.put(get_function_detail_url(function), data=function_data)
    assert response.status_code == 200

    function_data['state'] = Function.SENT_FOR_REVIEW
    response = user_api_client.patch(get_function_detail_url(function), data=function_data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_function_multivalued_attribute_not_allowed(function_data, user_api_client, function, free_text_attribute):
    set_permissions(user_api_client, Function.CAN_EDIT)

    function_data['function_id'] = function.classification.code
    function_data['attributes'] = {
        free_text_attribute.identifier: ['value1', 'value2']
    }

    response = user_api_client.put(get_function_detail_url(function), data=function_data)
    assert response.status_code == 200

    function_data['state'] = Function.SENT_FOR_REVIEW
    response = user_api_client.patch(get_function_detail_url(function), data=function_data)
    assert response.status_code == 400
    assert response.data['attributes'][free_text_attribute.identifier] == [
        'This attribute does not allow multiple values.']


@pytest.mark.parametrize('attributes', [
    'foo',
    ['foo'],
])
@pytest.mark.django_db
def test_function_put_invalid_attributes_format(function_data, user_api_client, function, attributes):
    function_data['function_id'] = function.classification.code
    function_data['phases'][0]['attributes'] = attributes
    response = user_api_client.put(get_function_detail_url(function), data=function_data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_function_state_change(user_api_client, function):
    set_permissions(user_api_client, Function.CAN_EDIT)
    data = {'state': Function.SENT_FOR_REVIEW, 'name': 'this should be ignored'}

    response = user_api_client.patch(get_function_detail_url(function), data=data)
    assert response.status_code == 200
    assert response.data['version'] == 1
    assert response.data['state'] == Function.SENT_FOR_REVIEW

    function.refresh_from_db()
    assert function.version == 1
    assert function.state == Function.SENT_FOR_REVIEW


@pytest.mark.django_db
def test_function_put_state(function_data, user_api_client, function):
    set_permissions(user_api_client, Function.CAN_EDIT)
    function_data['state'] = Function.SENT_FOR_REVIEW

    response = user_api_client.put(get_function_detail_url(function), data=function_data)
    assert response.status_code == 200

    new_function = Function.objects.last()
    assert new_function.state == Function.DRAFT


@pytest.mark.django_db
def test_state_change_validity(user_api_client, function):
    set_permissions(user_api_client, (Function.CAN_EDIT, Function.CAN_REVIEW, Function.CAN_APPROVE,
                                      'metarecord.delete_function'))
    url = get_function_detail_url(function)

    all_states = {Function.DRAFT, Function.SENT_FOR_REVIEW, Function.WAITING_FOR_APPROVAL, Function.APPROVED}

    valid_changes = {
        Function.DRAFT: {Function.SENT_FOR_REVIEW, Function.DELETED},
        Function.SENT_FOR_REVIEW: {Function.WAITING_FOR_APPROVAL, Function.DRAFT},
        Function.WAITING_FOR_APPROVAL: {Function.APPROVED, Function.DRAFT},
        Function.APPROVED: {Function.DRAFT},
    }

    for old_state, valid_new_states in valid_changes.items():
        function.state = old_state
        function.save(update_fields=('state',))

        for new_state in valid_new_states:
            function.state = old_state
            function.save(update_fields=('state',))

            response = user_api_client.patch(url, data={'state': new_state})
            assert response.status_code == 200

        invalid_new_states = all_states - valid_new_states - {old_state}

        for new_state in invalid_new_states:
            function.state = old_state
            function.save(update_fields=('state',))

            response = user_api_client.patch(url, data={'state': new_state})
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
        function.save(update_fields=('state',))
        required_perm = required_perms[new_state]

        others_than_required_perm = all_permissions - {required_perm}
        set_permissions(user_api_client, others_than_required_perm)
        response = user_api_client.patch(url, data={'state': new_state})
        assert response.status_code == 403

        set_permissions(user_api_client, required_perm)
        response = user_api_client.patch(url, data={'state': new_state})
        assert response.status_code == 200

    # changes back to DRAFT
    for old_state in {Function.SENT_FOR_REVIEW, Function.WAITING_FOR_APPROVAL, Function.APPROVED}:
        function.state = old_state
        function.save(update_fields=('state',))
        required_perm = required_perms[old_state]

        others_than_required_perm = all_permissions - {required_perm}
        set_permissions(user_api_client, others_than_required_perm)
        response = user_api_client.patch(url, data={'state': Function.DRAFT})
        assert response.status_code == 403

        set_permissions(user_api_client, required_perm)
        response = user_api_client.patch(url, data={'state': Function.DRAFT})
        assert response.status_code == 200


@pytest.mark.django_db
def test_metadata_version(user_api_client, user_2_api_client, function, function_data):
    url = get_function_detail_url(function)
    set_permissions(user_api_client, Function.CAN_EDIT)
    set_permissions(user_2_api_client, Function.CAN_EDIT)
    function_data['valid_from'] = '2015-01-01'

    response = user_api_client.put(url, data=function_data)
    assert response.status_code == 200

    new_function = Function.objects.last()
    original_modified_at = new_function.modified_at
    assert new_function.metadata_versions.count() == 1
    metadata_version = new_function.metadata_versions.last()
    assert metadata_version.state == Function.DRAFT
    assert metadata_version.modified_at == original_modified_at
    assert metadata_version.modified_by == user_api_client.user
    assert metadata_version.valid_from == datetime.date(2015, 1, 1)
    assert metadata_version.valid_to is None

    response = user_2_api_client.patch(url, data={'state': Function.SENT_FOR_REVIEW, 'valid_to': '2016-01-01'})
    assert response.status_code == 200

    new_function = Function.objects.last()
    assert new_function.metadata_versions.count() == 2
    metadata_version = new_function.metadata_versions.last()
    assert metadata_version.state == Function.SENT_FOR_REVIEW
    assert metadata_version.modified_at == new_function.modified_at > original_modified_at
    assert metadata_version.modified_by == user_2_api_client.user
    assert metadata_version.valid_from is None
    assert metadata_version.valid_to == datetime.date(2016, 1, 1)


@pytest.mark.django_db
def test_function_put_no_permission(function_data, user_api_client, function):
    response = user_api_client.put(get_function_detail_url(function), data=function_data)
    assert response.status_code == 403
    assert 'No permission to edit.' in str(response.data)


@pytest.mark.django_db
def test_function_cannot_edit_states(function_data, user_api_client, function):
    set_permissions(user_api_client, Function.CAN_EDIT)

    for state in (Function.SENT_FOR_REVIEW, Function.WAITING_FOR_APPROVAL):
        function.state = state
        function.save(update_fields=('state',))

        response = user_api_client.put(get_function_detail_url(function), data=function_data)
        assert response.status_code == 400
        assert 'Cannot edit while in state' in str(response.data)


@pytest.mark.django_db
def test_function_modified_by(function, user_api_client, user):
    set_permissions(user_api_client, Function.CAN_VIEW_MODIFIED_BY)

    response = user_api_client.get(get_function_detail_url(function))
    assert response.status_code == 200
    assert response.data['modified_by'] is None

    function.modified_by = user
    function.save(update_fields=('modified_by',))

    response = user_api_client.get(get_function_detail_url(function))
    assert response.status_code == 200
    assert response.data['modified_by'] == '%s %s' % (user.first_name, user.last_name)


@pytest.mark.django_db
def test_function_anonymous_cannot_view_modified_by(function, api_client, user):
    function.modified_by = user
    function.save(update_fields=('modified_by',))

    response = api_client.get(get_function_detail_url(function))
    assert response.status_code == 200
    assert 'modified_by' not in response.data


@pytest.mark.django_db
def test_function_user_cannot_view_modified_by(function, user_api_client, user):
    function.modified_by = user
    function.save(update_fields=('modified_by',))

    response = user_api_client.get(get_function_detail_url(function))
    assert response.status_code == 200
    assert 'modified_by' not in response.data


@pytest.mark.django_db
def test_function_another_user_cannot_view_modified_by(function, user_2_api_client, user):
    function.modified_by = user
    function.save(update_fields=('modified_by',))

    response = user_2_api_client.get(get_function_detail_url(function))
    assert response.status_code == 200
    assert 'modified_by' not in response.data


@pytest.mark.django_db
def test_function_anonymous_user_cannot_delete(function_data, api_client, function):
    response = api_client.delete(get_function_detail_url(function))
    assert response.status_code == 401


@pytest.mark.django_db
def test_function_user_cannot_delete(function_data, user_api_client, function):
    response = user_api_client.delete(get_function_detail_url(function))
    assert response.status_code == 403


@pytest.mark.django_db
def test_function_user_can_delete_own(function_data, user, user_api_client, function):
    function.modified_by = user
    function.save()

    response = user_api_client.delete(get_function_detail_url(function))
    assert response.status_code == 204

    new_function = Function.objects.get(pk=function.id)
    assert new_function.state == Function.DELETED
    assert new_function.metadata_versions.filter(modified_by=user, state=Function.DELETED).exists(), \
        'No metadata version created when deleting.'


@pytest.mark.django_db
def test_function_user_cannot_delete_other_users(function_data, user_2, user_api_client, function):
    function.modified_by = user_2
    function.save()

    response = user_api_client.delete(get_function_detail_url(function))
    assert response.status_code == 403

    new_function = Function.objects.get(pk=function.id)
    assert new_function.state == Function.DRAFT


@pytest.mark.django_db
def test_function_super_user_can_delete(function_data, super_user_api_client, function):
    response = super_user_api_client.delete(get_function_detail_url(function))
    assert response.status_code == 204

    new_function = Function.objects.get(pk=function.id)
    assert new_function.state == Function.DELETED
    assert new_function.metadata_versions.filter(
        modified_by=super_user_api_client.user, state=Function.DELETED).exists(), \
        'No metadata version created when deleting.'


@pytest.mark.django_db
def test_attribute_get_list_and_detail(choice_attribute, choice_value_1, attribute_group, user_api_client):
    for url in (ATTRIBUTE_LIST_URL, get_attribute_detail_url(choice_attribute)):
        response = user_api_client.get(url)
        assert response.status_code == 200
        data = response.data['results'][0] if 'results' in response.data else response.data

        assert uuid.UUID(data['id']) == choice_attribute.id
        assert data['identifier'] == choice_attribute.identifier
        assert data['name'] == choice_attribute.name
        assert data['group'] == attribute_group.name

        assert len(data['values']) == 1
        value_datum = data['values'][0]
        assert uuid.UUID(value_datum['id']) == choice_value_1.id
        assert value_datum['value'] == choice_value_1.value


@pytest.mark.django_db
def test_attribute_validations_when_sent_for_review(
        super_user_api_client, function, phase, action, record, free_text_attribute, free_text_attribute_2,
        choice_attribute, choice_value_1, choice_value_2, choice_attribute_2, choice_value_2_1, choice_value_2_2
):

    # set free text attribute required and choice attribute allowed for every structural element
    for structural_element in (Function, Phase, Action, Record):
        structural_element._attribute_validations['allowed'] = [
            free_text_attribute.identifier,
            choice_attribute.identifier,
            choice_attribute_2.identifier,
        ]
        structural_element._attribute_validations['required'] = [free_text_attribute.identifier]
        structural_element._attribute_validations['conditionally_required'] = {
            choice_attribute_2.identifier: {
                choice_attribute.identifier: choice_value_2.value
            }
        }

    valid_attributes = {
        free_text_attribute.identifier: 'some value',
        choice_attribute.identifier: choice_value_1.value,
    }

    # the function is missing a conditionally required attribute
    function.attributes = {choice_attribute.identifier: choice_value_2.value}
    function.save(update_fields=('attributes',))

    # new phase with valid attributes
    Phase.objects.create(function=function, index=2, attributes=valid_attributes)

    # the action has a non allowed attribute
    action.attributes = {free_text_attribute_2.identifier: 'some value'}
    action.save(update_fields=('attributes',))

    # the record has a non allowed value
    record.attributes = {choice_attribute.identifier: choice_value_2_1.value}
    record.save(update_fields=('attributes',))

    # try to send the function for review
    response = super_user_api_client.patch(get_function_detail_url(function), data={'state': Function.SENT_FOR_REVIEW})
    assert response.status_code == 400
    errors = response.data

    # check function attribute errors
    check_attribute_errors(errors, free_text_attribute, 'required')
    check_attribute_errors(errors, choice_attribute_2, 'required')  # this should be the conditionally required one

    # check phase attribute errors
    assert errors['phases'][1] == {}  # this should be the new phase with valid attributes
    errors = errors['phases'][0]
    check_attribute_errors(errors, free_text_attribute, 'required')

    # check action attribute errors
    errors = errors['actions'][0]
    check_attribute_errors(errors, free_text_attribute, 'required')
    check_attribute_errors(errors, free_text_attribute_2, 'allowed')

    # check record attribute errors
    errors = errors['records'][0]
    check_attribute_errors(errors, free_text_attribute, 'required')
    check_attribute_errors(errors, choice_attribute, 'value')

    # make the action valid and to try to send the function for review again
    action.attributes = valid_attributes
    action.save(update_fields=('attributes',))
    response = super_user_api_client.patch(get_function_detail_url(function), data={'state': Function.SENT_FOR_REVIEW})
    assert response.status_code == 400
    errors = response.data

    # check that the action is valid and the record errors are still there
    action_errors = errors['phases'][0]['actions'][0]
    assert 'attributes' not in action_errors
    record_errors = action_errors['records'][0]
    check_attribute_errors(record_errors, free_text_attribute, 'required')
    check_attribute_errors(record_errors, choice_attribute, 'value')

    # make the record valid and try to send the function for review again
    record.attributes = valid_attributes
    record.save(update_fields=('attributes',))
    response = super_user_api_client.patch(get_function_detail_url(function), data={'state': Function.SENT_FOR_REVIEW})
    assert response.status_code == 400
    errors = response.data

    # the action and the record are valid, there should be only phase errors
    phase_errors = errors['phases'][0]
    check_attribute_errors(phase_errors, free_text_attribute, 'required')
    assert 'actions' not in phase_errors

    # check supposed valid case as well
    phase.attributes = valid_attributes
    phase.save(update_fields=('attributes',))
    function.attributes = valid_attributes
    function.save(update_fields=('attributes',))
    response = super_user_api_client.patch(get_function_detail_url(function), data={'state': Function.SENT_FOR_REVIEW})
    assert response.status_code == 200


@pytest.mark.django_db
def test_conditionally_required_attribute_not_allowed_when_not_required(
        monkeypatch, super_user_api_client, function, choice_attribute, choice_value_1, choice_attribute_2,
        choice_value_2_1, choice_value_2_2
):
    monkeypatch.setitem(Function._attribute_validations, 'allowed', [choice_attribute.identifier])
    monkeypatch.setitem(
        Function._attribute_validations,
        'conditionally_required',
        {
            choice_attribute.identifier: {
                choice_attribute_2.identifier: choice_value_2_2.value
            }
        }
    )

    function.attributes = {
        choice_attribute.identifier: choice_value_1.value,
        choice_attribute_2.identifier: choice_value_2_1.value
    }
    function.save(update_fields=('attributes',))

    response = super_user_api_client.patch(get_function_detail_url(function), data={'state': Function.SENT_FOR_REVIEW})
    assert response.status_code == 400
    errors = response.data

    check_attribute_errors(errors, choice_attribute, 'allowed')


@pytest.mark.django_db
def test_conditionally_disallowed_attributes(
        monkeypatch, super_user_api_client, function, choice_attribute, choice_value_1, choice_attribute_2,
        choice_value_2_1, choice_value_2_2
):
    monkeypatch.setitem(
        Function._attribute_validations,
        'allowed',
        [choice_attribute.identifier, choice_attribute_2.identifier]
    )
    monkeypatch.setitem(
        Function._attribute_validations,
        'required',
        [choice_attribute.identifier, choice_attribute_2.identifier]
    )
    monkeypatch.setitem(
        Function._attribute_validations,
        'conditionally_disallowed',
        {
            choice_attribute.identifier: {
                choice_attribute_2.identifier: choice_value_2_2.value
            }
        }
    )

    function.attributes = {
        choice_attribute.identifier: choice_value_1.value,
        choice_attribute_2.identifier: choice_value_2_2.value
    }
    function.save(update_fields=('attributes',))

    response = super_user_api_client.patch(get_function_detail_url(function), data={'state': Function.SENT_FOR_REVIEW})
    assert response.status_code == 400
    errors = response.data

    check_attribute_errors(errors, choice_attribute, 'allowed')

    function.attributes[choice_attribute_2.identifier] = choice_value_2_1.value
    function.save(update_fields=('attributes',))

    response = super_user_api_client.patch(get_function_detail_url(function), data={'state': Function.SENT_FOR_REVIEW})
    assert response.status_code == 200


@pytest.mark.django_db
def test_all_or_none_validation(monkeypatch, super_user_api_client, function, choice_attribute, choice_attribute_2,
                                choice_value_1):
    monkeypatch.setitem(
        Function._attribute_validations,
        'allowed',
        (choice_attribute.identifier, choice_attribute_2.identifier)
    )
    monkeypatch.setitem(
        Function._attribute_validations,
        'all_or_none',
        ((choice_attribute.identifier, choice_attribute_2.identifier),)
    )

    function.attributes = {
        choice_attribute.identifier: choice_value_1.value,
    }
    function.save(update_fields=('attributes',))

    response = super_user_api_client.patch(get_function_detail_url(function), data={'state': Function.SENT_FOR_REVIEW})
    assert response.status_code == 400
    errors = response.data
    check_attribute_errors(errors, choice_attribute_2, 'required')


@pytest.mark.django_db
def test_allow_values_outside_choices_validation(monkeypatch, super_user_api_client, function, choice_attribute,
                                                 choice_attribute_2, choice_value_1, choice_value_2_1):
    monkeypatch.setitem(
        Function._attribute_validations,
        'allowed',
        (choice_attribute.identifier, choice_attribute_2.identifier)
    )

    monkeypatch.setitem(
        Function._attribute_validations,
        'multivalued',
        (choice_attribute_2.identifier,)
    )

    function.attributes = {
        choice_attribute.identifier: 'foo',
        choice_attribute_2.identifier: [choice_value_2_1.value, 'bar']
    }
    function.save(update_fields=('attributes',))

    response = super_user_api_client.patch(get_function_detail_url(function), data={'state': Function.SENT_FOR_REVIEW})
    assert response.status_code == 400
    errors = response.data
    check_attribute_errors(errors, choice_attribute, 'Invalid value')
    check_attribute_errors(errors, choice_attribute_2, 'Invalid value')

    monkeypatch.setitem(
        Function._attribute_validations,
        'allow_values_outside_choices',
        (choice_attribute.identifier, choice_attribute_2.identifier)
    )

    response = super_user_api_client.patch(get_function_detail_url(function), data={'state': Function.SENT_FOR_REVIEW})
    assert response.status_code == 200


@pytest.mark.django_db
def test_function_patch_required_fields(function_data, user_api_client, function):
    set_permissions(user_api_client, Function.CAN_REVIEW)

    function.state = Function.SENT_FOR_REVIEW
    function.save(update_fields=('state',))

    response = user_api_client.patch(get_function_detail_url(function), data=function_data)
    assert response.status_code == 400
    assert '"state", "valid_from" or "valid_to" required.' in str(response.data)


@pytest.mark.django_db
def test_function_validation_date_validation(user_api_client, function, function_data):
    url = get_function_detail_url(function)
    set_permissions(user_api_client, (Function.CAN_EDIT, Function.CAN_REVIEW))
    function_data['valid_from'] = '2015-01-02'
    function_data['valid_to'] = '2015-01-01'

    response = user_api_client.put(url, data=function_data)
    assert response.status_code == 400
    assert '"valid_from" cannot be after "valid_to".' in str(response.data)

    response = user_api_client.patch(url, data=function_data)
    assert response.status_code == 400
    assert '"valid_from" cannot be after "valid_to".' in str(response.data)


@pytest.mark.parametrize('filtering, expected_indexes', (
        ('', [0, 1, 2, 3, 4]),
        ('valid_at=34234xyz', []),
        ('valid_at=1999-05-05', [4]),
        ('valid_at=2000-05-05', [1, 4]),
        ('valid_at=2004-05-05', [1, 2, 3, 4]),
        ('valid_at=2007-05-05', [1]),
))
@pytest.mark.django_db
def test_function_validation_date_filtering(user_api_client, filtering, expected_indexes):
    classifications = [
        Classification.objects.get_or_create(code=code)[0]
        for code in ('00', '01', '02', '03', '04')
    ]
    functions = (
        Function.objects.create(classification=classifications[0]),
        Function.objects.create(classification=classifications[1], valid_from='2000-05-05'),
        Function.objects.create(classification=classifications[2], valid_from='2002-05-05', valid_to='2004-05-05'),
        Function.objects.create(classification=classifications[3], valid_from='2003-05-05', valid_to='2005-05-05'),
        Function.objects.create(classification=classifications[4], valid_to='2006-05-05'),
    )

    response = user_api_client.get(FUNCTION_LIST_URL + '?' + filtering)
    assert response.status_code == 200
    assert_response_functions(response, [functions[index] for index in expected_indexes])


@pytest.mark.parametrize('filtering, expected_indexes', (
    ('', [0, 1, 2, 3, 4]),
    ('modified_at__lt=34234xyz', []),
    ('modified_at__lt=1999-05-05 00:00:00', [0]),
    ('modified_at__lt=2000-05-05 00:00:00', [0]),
    ('modified_at__lt=2001-05-05 13:00:00', [0,1]),
    ('modified_at__lt=2004-05-05 00:00:00', [0, 1, 2, 3]),
    ('modified_at__lt=2007-05-05 00:00:00', [0, 1, 2, 3, 4]),
    ('modified_at__gt=34234xyz', []),
    ('modified_at__gt=1999-05-05 00:00:00', [1, 2, 3, 4]),
    ('modified_at__gt=2000-05-05 00:00:00', [1, 2, 3, 4]),
    ('modified_at__gt=2001-05-05 13:00:00', [2, 3, 4]),
    ('modified_at__gt=2004-05-05 00:00:00', [4]),
    ('modified_at__gt=2007-05-05 00:00:00', []),
    ('modified_at__gt=1970-01-01 00:00:00&modified_at__lt=1971-05-05 00:00:00', [0]),
    ('modified_at__gt=2000-05-05 00:00:00&modified_at__lt=2000-05-05 00:00:00', []),
    ('modified_at__gt=2010-05-05 00:00:00&modified_at__lt=2000-05-05 00:00:00', []),
    ('modified_at__gt=2002-05-05 00:00:00&modified_at__lt=2004-05-05 00:00:00', [2, 3]),
    ('modified_at__gt=1970-05-05 00:00:00&modified_at__lt=2010-05-05 00:00:00', [1, 2, 3, 4]),
))
@pytest.mark.django_db
def test_function_validation_modified_at_filtering(user_api_client, filtering, expected_indexes):
    classifications = [
        Classification.objects.get_or_create(code=code)[0]
        for code in ('00', '01', '02', '03', '04')
    ]
    modified_at_values = [
        pytz.utc.localize(datetime.datetime(year=1970, month=1, day=1, hour=12, minute=0, second=0)),
        pytz.utc.localize(datetime.datetime(year=2000, month=5, day=5, hour=12, minute=0, second=0)),
        pytz.utc.localize(datetime.datetime(year=2002, month=5, day=5, hour=12, minute=0, second=0)),
        pytz.utc.localize(datetime.datetime(year=2003, month=5, day=5, hour=12, minute=0, second=0)),
        pytz.utc.localize(datetime.datetime(year=2006, month=5, day=5, hour=12, minute=0, second=0)),
    ]
    functions = []
    for i, modified_at_value in enumerate(modified_at_values):
        function = Function.objects.create(classification=classifications[i])
        Function.objects.filter(pk=function.pk).update(modified_at=modified_at_value)
        functions.append(Function.objects.get(pk=function.pk))

    response = user_api_client.get(FUNCTION_LIST_URL + '?' + filtering)
    assert response.status_code == 200
    assert_response_functions(response, [functions[index] for index in expected_indexes])


@pytest.mark.django_db
def test_name_field(user_api_client, function, phase, action, record):
    url = get_function_detail_url(function)

    response = user_api_client.get(url)
    assert response.status_code == 200
    data = response.data

    # expect name to match TypeSpecifier
    assert data['phases'][0]['name'] == phase.attributes['TypeSpecifier']
    assert data['phases'][0]['actions'][0]['name'] == action.attributes['TypeSpecifier']
    assert data['phases'][0]['actions'][0]['records'][0]['name'] == record.attributes['TypeSpecifier']

    phase.attributes = {'PhaseType': 'phase_type'}
    action.attributes = {'ActionType': 'action_type'}
    record.attributes = {'RecordType':  'record_type'}
    phase.save()
    action.save()
    record.save()

    response = user_api_client.get(url)
    assert response.status_code == 200
    data = response.data

    # no TypeSpecifier, expect name to match type
    assert data['phases'][0]['name'] == phase.attributes['PhaseType']
    assert data['phases'][0]['actions'][0]['name'] == action.attributes['ActionType']
    assert data['phases'][0]['actions'][0]['records'][0]['name'] == record.attributes['RecordType']


@pytest.mark.parametrize('endpoint', ('list', 'detail'))
@pytest.mark.django_db
def test_attribute_endpoints(user_api_client, choice_attribute, choice_value_1, attribute_group, endpoint):
    url = ATTRIBUTE_LIST_URL if endpoint == 'list' else get_attribute_detail_url(choice_attribute)

    response = user_api_client.get(url)
    assert response.status_code == 200

    if endpoint == 'list':
        results = response.data['results']
        assert len(results) == 1
        attribute_data = results[0]
    else:
        attribute_data = response.data

    assert attribute_data.keys() == {
        'name', 'values', 'id', 'created_at', 'modified_at', 'help_text', 'group', 'identifier', 'index'
    }
    assert attribute_data['name'] == choice_attribute.name
    assert attribute_data['identifier'] == choice_attribute.identifier
    assert attribute_data['help_text'] == choice_attribute.help_text
    assert attribute_data['group'] == attribute_group.name
    assert len(attribute_data['values']) == 1

    value_data = attribute_data['values'][0]
    assert value_data.keys() == {'id', 'value', 'created_at', 'modified_at', 'index'}
    assert value_data['value'] == choice_value_1.value


@pytest.mark.parametrize('filtering, expected_indexes', (
        ('', [2, 3]),
        ('version=', [2, 3]),
        ('version=foo', []),
        ('version=1', [0, 3]),
        ('version=2', [1]),
))
@pytest.mark.django_db
def test_function_version_filter(user_api_client, filtering, expected_indexes, classification, classification_2):
    functions = (
        Function.objects.create(classification=classification),
        Function.objects.create(classification=classification),
        Function.objects.create(classification=classification),
        Function.objects.create(classification=classification_2),
    )

    response = user_api_client.get(FUNCTION_LIST_URL + '?' + filtering)
    assert response.status_code == 200
    assert_response_functions(response, [functions[index] for index in expected_indexes])


@pytest.mark.django_db
def test_classification_function_field(user_api_client, classification, classification_2):
    function = Function.objects.create(classification=classification)
    Function.objects.create(classification=classification)
    Function.objects.create(classification=classification_2)
    classification_3 = Classification.objects.create(code='05')

    response = user_api_client.get(CLASSIFICATION_LIST_URL)
    assert response.status_code == 200
    assert response.data['results'][0]['function'] == function.uuid.hex
    assert response.data['results'][2]['function'] is None

    response = user_api_client.get(get_classification_detail_url(classification))
    assert response.status_code == 200
    assert response.data['function'] == function.uuid.hex

    response = user_api_client.get(get_classification_detail_url(classification_3))
    assert response.status_code == 200
    assert response.data['function'] is None


@pytest.mark.django_db
def test_function_version_history_field(user_api_client, classification):
    functions = (
        Function.objects.create(classification=classification),
        Function.objects.create(classification=classification),
        Function.objects.create(classification=classification),
    )
    Function.objects.filter(id=functions[2].id).update(
        state=Function.SENT_FOR_REVIEW, modified_by=user_api_client.user
    )

    response = user_api_client.get(FUNCTION_LIST_URL)
    assert response.status_code == 200
    assert 'version_history' not in response.data['results'][0]

    response = user_api_client.get(get_function_detail_url(functions[2]))
    assert response.status_code == 200
    version_history = response.data['version_history']

    assert len(version_history) == 3

    first_version = version_history[0]
    assert first_version.get('modified_at')
    assert first_version['state'] == 'draft'
    assert first_version['version'] == 1
    assert 'modified_by' not in version_history[0]

    last_version = version_history[2]
    assert last_version['state'] == 'sent_for_review'
    assert last_version['version'] == 3

    set_permissions(user_api_client, Function.CAN_VIEW_MODIFIED_BY)

    response = user_api_client.get(get_function_detail_url(functions[2]))
    assert response.status_code == 200
    version_history = response.data['version_history']

    first_version = version_history[0]
    assert first_version['modified_by'] is None

    last_version = version_history[2]
    assert last_version['modified_by'] == 'John Rambo'
