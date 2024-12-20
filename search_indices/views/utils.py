from search_indices.serializers.utils import attributes_for_authenticated


def populate_filter_fields_with_attributes(
    filter_fields: dict, attributes: list, exclude_information_system: bool = False
) -> None:
    """
    Fetch the filter fields from the indexed attributes.
    """
    if not attributes:
        return

    if exclude_information_system:
        for attribute in attributes_for_authenticated:
            filter_fields.pop(attribute, None)

    for attribute in attributes:
        attribute_replaced = attribute.replace(".", "+")
        # Example {"Subject.Scheme": "attributes.Subject+Scheme"}
        filter_fields[attribute] = f"attributes.{attribute_replaced}"
