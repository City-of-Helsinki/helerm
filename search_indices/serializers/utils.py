from typing import Optional

from elasticsearch_dsl.response.hit import Hit

attributes_for_authenticated = (
    "function_InformationSystem",
    "action_InformationSystem",
    "classification_InformationSystem",
    "record_InformationSystem",
    "phase_InformationSystem",
)


def get_attributes(
    obj: Hit, attribute_field_name: str, authenticated: bool
) -> Optional[dict]:
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

            if not authenticated and key in attributes_for_authenticated:
                continue

            attributes[key] = value

        return attributes
    return None
