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
        old_value = old.get(key, None)

        if (isinstance(old_value, dict) and
                isinstance(new_value, dict)):
            old[key] = update_nested_dictionary(old_value, new_value)
        else:
            old[key] = new_value

    return old
