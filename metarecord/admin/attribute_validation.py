from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_admin_json_editor import JSONEditorWidget

from metarecord.models.attribute import Attribute, AttributeValue
from metarecord.models.attribute_validation import AttributeValidationRule


def dynamic_schema(widget):
    """
    Dynamic schema created with: https://github.com/abogushov/django-admin-json-editor.
    Example dynamic schemas can be found here: https://github.com/json-editor/json-editor.
    """
    attribute_identifiers = list(
        Attribute.objects.order_by("index", "identifier").values_list(
            "identifier", flat=True
        )
    )
    attribute_names = list(
        Attribute.objects.order_by("index", "identifier").values_list("name", flat=True)
    )
    attribute_values = list(
        AttributeValue.objects.order_by("value").values_list("value", flat=True)
    )

    return {
        "type": "object",
        "title": str(_("Attribute validation rules")),
        "properties": {
            "allowed": {
                "title": str(_("Allowed")),
                "type": "array",
                "items": {
                    "title": str(_("Allowed")),
                    "type": "string",
                    "enum": attribute_identifiers,
                    "options": {
                        "enum_titles": attribute_names,
                    },
                },
            },
            "required": {
                "title": str(_("Required")),
                "type": "array",
                "items": {
                    "title": str(_("Required")),
                    "type": "string",
                    "enum": attribute_identifiers,
                    "options": {
                        "enum_titles": attribute_names,
                    },
                },
            },
            "conditionally_required": {
                "title": str(_("Conditionally Required")),
                "type": "array",
                "items": {
                    "title": str(_("Conditionally Required")),
                    "type": "object",
                    "properties": {
                        "attribute": {
                            "title": str(_("Attribute")),
                            "type": "string",
                            "enum": attribute_identifiers,
                            "options": {
                                "enum_titles": attribute_names,
                            },
                        },
                        "conditions": {
                            "title": str(_("Required Conditions")),
                            "type": "array",
                            "items": {
                                "title": str(_("Required Condition")),
                                "type": "object",
                                "properties": {
                                    "attribute": {
                                        "title": str(_("Attribute")),
                                        "type": "string",
                                        "enum": attribute_identifiers,
                                        "options": {
                                            "enum_titles": attribute_names,
                                        },
                                    },
                                    "value": {
                                        "title": str(_("Value")),
                                        "type": "string",
                                        "enum": attribute_values,
                                    },
                                },
                                "required": ["attribute", "value"],
                            },
                        },
                    },
                    "required": ["attribute", "conditions"],
                },
            },
            "conditionally_disallowed": {
                "title": str(_("Conditionally Disallowed")),
                "type": "array",
                "items": {
                    "title": str(_("Conditionally Disallowed")),
                    "type": "object",
                    "properties": {
                        "attribute": {
                            "title": str(_("Attribute")),
                            "type": "string",
                            "enum": attribute_identifiers,
                            "options": {
                                "enum_titles": attribute_names,
                            },
                        },
                        "conditions": {
                            "title": str(_("Disallowed Conditions")),
                            "type": "array",
                            "items": {
                                "title": str(_("Disallowed Condition")),
                                "type": "object",
                                "properties": {
                                    "attribute": {
                                        "title": str(_("Attribute")),
                                        "type": "string",
                                        "enum": attribute_identifiers,
                                        "options": {
                                            "enum_titles": attribute_names,
                                        },
                                    },
                                    "value": {
                                        "title": str(_("Value")),
                                        "type": "string",
                                        "enum": attribute_values,
                                    },
                                },
                                "required": ["attribute", "value"],
                            },
                        },
                    },
                    "required": ["attribute", "conditions"],
                },
            },
            "multivalued": {
                "title": str(_("Multivalued")),
                "type": "array",
                "items": {
                    "title": str(_("Multivalued")),
                    "type": "string",
                    "enum": attribute_identifiers,
                    "options": {
                        "enum_titles": attribute_names,
                    },
                },
            },
            "all_or_none": {
                "title": str(_("All or None")),
                "type": "array",
                "items": {
                    "title": str(_("Attribute set")),
                    "type": "array",
                    "items": {
                        "title": str(_("Attribute")),
                        "type": "string",
                        "enum": attribute_identifiers,
                        "options": {
                            "enum_titles": attribute_names,
                        },
                    },
                },
            },
            "allow_values_outside_choices": {
                "title": str(_("Values Outside Choices")),
                "type": "array",
                "items": {
                    "title": str(_("Values Outside Choices")),
                    "type": "string",
                    "enum": attribute_identifiers,
                    "options": {
                        "enum_titles": attribute_names,
                    },
                },
            },
        },
        "required": [
            "allowed",
            "required",
            "conditionally_required",
            "conditionally_disallowed",
            "multivalued",
            "all_or_none",
            "allow_values_outside_choices",
        ],
    }


@admin.register(AttributeValidationRule)
class AttributeValidationRuleAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        widget = JSONEditorWidget(dynamic_schema, collapsed=False)
        form = super().get_form(
            request, obj, widgets={"validation_json": widget}, **kwargs
        )
        return form
