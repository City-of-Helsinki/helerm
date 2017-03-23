from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

from .base import TimeStampedModel, UUIDPrimaryKeyModel
from .predefined_attributes import PREDEFINED_ATTRIBUTES


class AttributeGroup(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('name'))

    class Meta:
        verbose_name = _('attribute group')
        verbose_name_plural = _('attribute groups')

    def __str__(self):
        return self.name


class Attribute(TimeStampedModel, UUIDPrimaryKeyModel):
    identifier = models.CharField(verbose_name=_('identifier'), max_length=64, unique=True, db_index=True)
    name = models.CharField(verbose_name=_('name'), max_length=256)
    index = models.PositiveSmallIntegerField(db_index=True)
    group = models.ForeignKey(AttributeGroup, verbose_name=_('group'), related_name='attributes', null=True, blank=True)

    class Meta:
        verbose_name = _('attribute')
        verbose_name_plural = _('attributes')
        ordering = ('index',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = self.pk
        if not self.index:
            self.index = max(Attribute.objects.values_list('index', flat=True) or [0]) + 1
        super().save(*args, **kwargs)

    def is_free_text(self):
        return not self.values.exists()


class AttributeValue(TimeStampedModel, UUIDPrimaryKeyModel):
    attribute = models.ForeignKey(Attribute, verbose_name=_('attribute'), related_name='values')
    value = models.CharField(verbose_name=_('value'), max_length=1024)

    class Meta:
        verbose_name = _('attribute value')
        verbose_name_plural = _('attribute values')
        unique_together = ('attribute', 'value')

    def __str__(self):
        return self.value


def create_predefined_attributes():
    with transaction.atomic():
        for attribute in PREDEFINED_ATTRIBUTES:
            Attribute.objects.get_or_create(identifier=attribute['identifier'], defaults=attribute)
