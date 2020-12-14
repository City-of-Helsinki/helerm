from typing import Optional

from elasticsearch_dsl.response.hit import Hit


def get_attributes(obj: Hit, attribute_field_name: str) -> Optional[dict]:
    """
    Fetch attributes from index and revert the attribute names that
    have "." replaced with "+".
    """
    attrs = getattr(obj, attribute_field_name)
    if attrs:
        attributes = {}
        attrs = attrs.to_dict()
        for key, value in attrs.items():
            key = key.replace("+", ".")
            attributes[key] = value
        return attributes
    return None
