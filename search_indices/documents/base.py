from typing import Optional

from django_elasticsearch_dsl import Document, fields

import search_indices
from metarecord.models import Action, Classification, Function, Phase, StructuralElement
from search_indices.documents.utils import prepare_attributes


class BaseDocument(Document):
    id = fields.KeywordField(attr="uuid.hex")
    title = fields.TextField(
        analyzer=search_indices.FINNISH_ANALYZER,
        fields={"keyword": fields.KeywordField()},
    )
    description = fields.TextField(
        analyzer=search_indices.FINNISH_ANALYZER,
        fields={"keyword": fields.KeywordField()},
    )
    description_internal = fields.TextField(
        analyzer=search_indices.FINNISH_ANALYZER,
        fields={"keyword": fields.KeywordField()},
    )
    additional_information = fields.TextField(
        analyzer=search_indices.FINNISH_ANALYZER,
        fields={"keyword": fields.KeywordField()},
    )
    state = fields.KeywordField()
    code = fields.KeywordField()
    type = fields.IntegerField()
    parent = fields.ObjectField(
        properties={
            "id": fields.KeywordField(attr="uuid.hex"),
            "title": fields.KeywordField(),
            "version": fields.IntegerField(),
        }
    )
    attributes = fields.ObjectField(dynamic=True)

    def prepare_title(self, obj: StructuralElement) -> Optional[str]:
        title = getattr(obj, "title", None)
        if not title:
            title = getattr(obj, "name", None)
        return title

    def prepare_description(self, obj: StructuralElement) -> Optional[str]:
        return getattr(obj, "description", None)

    def prepare_description_internal(self, obj: StructuralElement) -> Optional[str]:
        return getattr(obj, "description_internal", None)

    def prepare_additional_information(self, obj: StructuralElement) -> Optional[str]:
        return getattr(obj, "additional_information", None)

    def prepare_state(self, obj: StructuralElement) -> Optional[str]:
        return getattr(obj, "state", None)

    def prepare_code(self, obj: StructuralElement) -> Optional[str]:
        return getattr(obj, "code", None)

    def prepare_type(self, obj: StructuralElement) -> int:
        obj_type = type(obj)
        if obj_type == Classification:
            return 1
        elif obj_type == Function:
            return 2
        elif obj_type == Phase:
            return 3
        elif obj_type == Action:
            return 4
        return 5

    def prepare_parent(self, obj: StructuralElement) -> Optional[dict]:
        parent = getattr(obj, "parent", None)
        if parent:
            return {
                "id": parent.uuid.hex,
                "title": self.prepare_title(parent),
                "version": getattr(parent, "version", None),
            }
        return None

    def prepare_attributes(self, obj: Function) -> Optional[dict]:
        if hasattr(obj, "attributes"):
            model_name = str(self.Django.model._meta.verbose_name)
            return prepare_attributes(obj, prefix=f"{model_name}_")
        return None
