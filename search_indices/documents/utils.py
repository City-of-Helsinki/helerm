from metarecord.models.structural_element import StructuralElement


def prepare_attributes(obj: StructuralElement, prefix: str = "") -> dict:
    """
    ElasticSearch cannot handle attribute names with dots, for example "Subject.Scheme".
    This is because it tries to interpret Scheme as an attribute for Subject.
    Fix this by replacing "." with "+" when indexing the Documents.
    """
    attributes = {}
    if obj:
        attrs = obj.attributes
        for key, value in attrs.items():
            key = key.replace(".", "+")
            attributes[prefix + key] = str(value)
    return attributes
