def populate_filter_fields_with_attributes(
    filter_fields: dict, attributes: list
) -> None:
    """
    Fetch the filter fields from the indexed attributes.
    """
    if not attributes:
        return
    for attribute in attributes:
        attribute_replaced = attribute.replace(".", "+")
        # Example {"Subject.Scheme": "attributes.Subject+Scheme"}
        filter_fields[attribute] = f"attributes.{attribute_replaced}"
