import datetime
import uuid
import pytest
from rest_framework.reverse import reverse
from metarecord.models import Action, Attribute, Function, Phase, Record
from metarecord.tests.utils import assert_response_functions, check_attribute_errors, set_permissions


FUNCTION_LIST_URL = reverse('v1:function-list')
ATTRIBUTE_LIST_URL = reverse('v1:attribute-list')


def get_function_detail_url(function):
    return reverse('v1:function-detail', kwargs={'uuid': function.uuid})


def get_attribute_detail_url(attribute):
    return reverse('v1:attribute-detail', kwargs={'pk': attribute.id})


@pytest.fixture
def function_data(parent_function, function, free_text_attribute, choice_attribute):
    return {
        'name': 'new function',
        'function_id': function.function_id,
        'parent': parent_function.uuid,
        'attributes': {
            free_text_attribute.identifier: 'new function attribute value',
        },
        'phases': [
            {
                'name': 'new phase',
                'actions': [
                    {
                        'name': 'new action',
                        'records': [
                            {
                                'name': 'new record',
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
def disable_attribute_validations():
    for structural_element in (Function, Phase, Action, Record):
        structural_element._attribute_validations['allowed'] = None
        structural_element._attribute_validations['required'] = None
        structural_element._attribute_validations['conditionally_required'] = None


def _check_function_object_matches_data(function_obj, data):
    new_function = function_obj

    assert new_function.parent == Function.objects.latest_version().get(uuid=data['parent'])
    assert new_function.name == data['name']
    assert new_function.attributes == data['attributes']
    assert new_function.phases.count() == 1

    new_phase = new_function.phases.first()
    phase_data = data['phases'][0]
    assert new_phase.name == phase_data['name']
    assert new_phase.attributes == {}
    assert new_phase.actions.count() == 1

    new_action = new_phase.actions.first()
    action_data = phase_data['actions'][0]
    assert new_action.name == action_data['name']
    assert new_action.attributes == {}
    assert new_action.records.count() == 1

    new_record = new_action.records.first()
    record_data = action_data['records'][0]
    assert new_record.name == record_data['name']
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
])
@pytest.mark.django_db
def test_get(api_client, resource, function, phase, action, record, attribute, template):
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
def test_function_versioning(api_client):
    first_draft = Function.objects.create(name='first draft', function_id='00 00')
    first_approved = Function.objects.create(name='first approved', function_id='00 00', state=Function.APPROVED)
    second_approved = Function.objects.create(name='second approved', function_id='00 00', state=Function.APPROVED)
    second_draft = Function.objects.create(name='second draft', function_id='00 00')
    other_function = Function.objects.create(name='other function', function_id='00 01')
    template = Function.objects.create(name='template', is_template=True)

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
    assert response.data['name'] == 'second draft'

    # /function/<uuid>/?state=approved should return the latest approved version
    response = api_client.get(url + '?state=approved')
    assert response.status_code == 200
    assert response.data['name'] == 'second approved'


@pytest.mark.django_db
def test_unauthenticated_user_cannot_post_or_put_functions(function_data, api_client, function):
    response = api_client.post(FUNCTION_LIST_URL, data=function_data)
    assert response.status_code == 401

    response = api_client.put(get_function_detail_url(function), data=function_data)
    assert response.status_code == 401


@pytest.mark.django_db
def test_cannot_post_or_delete_functions(user_api_client, function, function_data):
    response = user_api_client.post(FUNCTION_LIST_URL, data=function_data)
    assert response.status_code == 405

    response = user_api_client.delete(get_function_detail_url(function))
    assert response.status_code == 405


@pytest.mark.django_db
def test_function_put(function_data, user_api_client, function, phase, action, record):
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
    function_data['function_id'] = function.function_id
    function_data['attributes'] = {'InvalidFunctionAttribute': 'value'}
    function_data['phases'][0]['attributes'] = {'InvalidPhaseAttribute': 'value'}

    response = user_api_client.put(get_function_detail_url(function), data=function_data)
    assert response.status_code == 400
    assert response.data['attributes']['InvalidFunctionAttribute'] == ['Invalid attribute.']
    assert response.data['phases'][0]['attributes']['InvalidPhaseAttribute'] == ['Invalid attribute.']


@pytest.mark.parametrize('attributes', [
    'foo',
    ['foo'],
    {'ChoiceAttr': ['foo']},
])
@pytest.mark.django_db
def test_function_put_invalid_attributes_format(function_data, user_api_client, function, attributes):
    function_data['function_id'] = function.function_id
    function_data['phases'][0]['attributes'] = attributes
    response = user_api_client.put(get_function_detail_url(function), data=function_data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_function_state_change(user_api_client, function):
    set_permissions(user_api_client, Function.CAN_EDIT)
    data = {'state': Function.SENT_FOR_REVIEW, 'name': 'this should be ignored'}
    original_name = function.name

    response = user_api_client.patch(get_function_detail_url(function), data=data)
    assert response.status_code == 200
    assert response.data['version'] == 1
    assert response.data['state'] == Function.SENT_FOR_REVIEW
    assert response.data['name'] == original_name

    function.refresh_from_db()
    assert function.version == 1
    assert function.state == Function.SENT_FOR_REVIEW
    assert function.name == original_name


@pytest.mark.django_db
def test_function_put(function_data, user_api_client, function):
    set_permissions(user_api_client, Function.CAN_EDIT)
    function_data['state'] = Function.SENT_FOR_REVIEW

    response = user_api_client.put(get_function_detail_url(function), data=function_data)
    assert response.status_code == 200

    new_function = Function.objects.last()
    assert new_function.state == Function.DRAFT


@pytest.mark.django_db
def test_state_change_validity(user_api_client, function):
    set_permissions(user_api_client, (Function.CAN_EDIT, Function.CAN_REVIEW, Function.CAN_APPROVE))
    url = get_function_detail_url(function)

    all_states = {Function.DRAFT, Function.SENT_FOR_REVIEW, Function.WAITING_FOR_APPROVAL, Function.APPROVED}

    valid_changes = {
        Function.DRAFT: {Function.SENT_FOR_REVIEW},
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
    response = user_api_client.get(get_function_detail_url(function))
    assert response.status_code == 200
    assert response.data['modified_by'] is None

    function.modified_by = user
    function.save(update_fields=('modified_by',))

    response = user_api_client.get(get_function_detail_url(function))
    assert response.status_code == 200
    assert response.data['modified_by'] == '%s %s' % (user.first_name, user.last_name)


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
        choice_attribute, choice_value_1, choice_attribute_2, choice_value_2_1, choice_value_2_2
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
            choice_attribute.identifier: {
                choice_attribute_2.identifier: choice_value_2_2.value
            }
        }

    valid_attributes = {
        free_text_attribute.identifier: 'some value',
        choice_attribute.identifier: choice_value_1.value,
    }

    # the function has a conditionally required attribute
    function.attributes = {choice_attribute_2.identifier: choice_value_2_2.value}
    function.save(update_fields=('attributes',))

    # new phase with valid attributes
    Phase.objects.create(function=function, name='phase 2', index=2, attributes=valid_attributes)

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
    check_attribute_errors(errors, choice_attribute, 'required')  # this should be the conditionally required one

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
    functions = (
        Function.objects.create(
            name='function_0', function_id='00'
        ),
        Function.objects.create(
            name='function_1', function_id='01', valid_from='2000-05-05'
        ),
        Function.objects.create(
            name='function_2', function_id='02', valid_from='2002-05-05', valid_to='2004-05-05'
        ),
        Function.objects.create(
            name='function_3', function_id='03', valid_from='2003-05-05', valid_to='2005-05-05'
        ),
        Function.objects.create(
            name='function_4', function_id='04', valid_to='2006-05-05'
        ),
    )

    response = user_api_client.get(FUNCTION_LIST_URL + '?' + filtering)
    assert response.status_code == 200
    assert_response_functions(response, [functions[index] for index in expected_indexes])
