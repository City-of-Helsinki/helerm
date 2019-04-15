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
