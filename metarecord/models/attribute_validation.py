from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from metarecord.models.base import TimeStampedModel, UUIDPrimaryKeyModel


class AttributeValidationRule(TimeStampedModel, UUIDPrimaryKeyModel):
    content_type = models.OneToOneField(
        ContentType,
        verbose_name=_("content type"),
        on_delete=models.CASCADE,
        limit_choices_to=Q(model="action")
        | Q(model="function")
        | Q(model="phase")
        | Q(model="record")
        | Q(model="attributevalidationrule"),
        help_text=_(
            "Relation to the chosen type: Action (Toimenpide) / Function"
            " (Käsittelyprosessi) / Phase (Käsittelyvaihe) / Record (Asiakirja)."
            " Relation to 'Attribute validation rule' is applied for each of the types."
        ),
    )
    validation_json = models.JSONField()

    class Meta:
        verbose_name = _("attribute validation rule")
        verbose_name_plural = _("attribute validation rules")
        ordering = ("content_type",)

    def __str__(self):
        return f"{self.content_type}"
