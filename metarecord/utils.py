from uuid import UUID

from django.db import transaction

from metarecord.models import Action, Function, Phase, Record


def model_to_dict(instance, fields=None, exclude=None):
    """
    Return a dict containing the data in instance.

    This differs from django.forms.model_to_dict by containing non-editable
    fields and relation values being the related objects instead of pk of those
    objects.

    :param instance: Model instance
    :param fields: list of fields in dict
    :param exclude: list of fields not in dict
    :return: dictionary of instance fields and values
    """
    data = {}
    for field in instance._meta.fields:
        if fields and field.name not in fields:
            continue
        if exclude and field.name in exclude:
            continue
        data[field.name] = getattr(instance, field.name)
    return data


@transaction.atomic
def create_new_function_version(function, user):
    user_data = {'created_by': user, 'modified_by': user}

    function_data = model_to_dict(function, exclude=('id', 'bulk_update'))
    function_data.update(user_data)
    new_function = Function.objects.create(**function_data)

    for phase in function.phases.all():
        phase_data = model_to_dict(phase, exclude=('id', 'function'))
        phase_data.update(user_data)
        new_phase = Phase.objects.create(function=new_function, **phase_data)

        for action in phase.actions.all():
            action_data = model_to_dict(action, exclude=('id', 'phase'))
            action_data.update(user_data)
            new_action = Action.objects.create(phase=new_phase, **action_data)

            for record in action.records.all():
                record_data = model_to_dict(record, exclude=('id', 'action'))
                record_data.update(user_data)
                Record.objects.create(action=new_action, **record_data)

    return new_function


def update_nested_dictionary(old, new):
    """
    Update dictionary with the values from other dictionary. Recursively update
    any nested dictionaries if both old and new values are dictionaries.

    :param old: Old dictionary that will be updated
    :type old: dict
    :param new: New dictionary that contains the updated values
    :type new: dict
    :return: Updated dictionary
    :rtype: dict
    """
    for key, new_value in new.items():
        old_value = old.get(key)

        if (isinstance(old_value, dict) and
                isinstance(new_value, dict)):
            old[key] = update_nested_dictionary(old_value, new_value)
        else:
            old[key] = new_value

    return old


def validate_uuid4(string):
    try:
        UUID(string, version=4)
    except (AttributeError, ValueError, TypeError):
        return False
    else:
        return True
