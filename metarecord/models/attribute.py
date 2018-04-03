import logging

from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

from .base import TimeStampedModel, UUIDPrimaryKeyModel
from .predefined_attributes import PREDEFINED_ATTRIBUTES

logger = logging.getLogger(__name__)


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
    group = models.ForeignKey(
        AttributeGroup, verbose_name=_('group'), related_name='attributes', null=True, blank=True,
        on_delete=models.SET_NULL
    )
    help_text = models.TextField(verbose_name=_('help text'), blank=True)

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

    @classmethod
    def check_identifiers(cls, identifiers):
        """
        Check that identifiers are valid.

        :param identifiers: list of identifiers
        :return: validation error dict
        """

        errors = {}
        valid_identifiers = set(Attribute.objects.values_list('identifier', flat=True))
        invalid_identifiers = set(identifiers) - valid_identifiers
        if invalid_identifiers:
            errors = {identifier: [_('Invalid attribute.')] for identifier in invalid_identifiers}
        return errors

    def is_free_text(self):
        return not self.values.exists()


class AttributeValue(TimeStampedModel, UUIDPrimaryKeyModel):
    attribute = models.ForeignKey(
        Attribute, verbose_name=_('attribute'), related_name='values', on_delete=models.CASCADE
    )
    value = models.CharField(verbose_name=_('value'), max_length=1024)
    index = models.PositiveSmallIntegerField(db_index=True)

    class Meta:
        verbose_name = _('attribute value')
        verbose_name_plural = _('attribute values')
        unique_together = ('attribute', 'value')
        ordering = ('index',)

    def __str__(self):
        return self.value

    def save(self, *args, **kwargs):
        if not self.index:
            # in theory a race condition is possible here, but with current usage
            # that is practically impossible, and it won't cause any real harm anyway
            last_index = (
                AttributeValue.objects
                .filter(attribute=self.attribute)
                .values_list('index', flat=True)
                .last()
            )
            self.index = last_index + 1 if last_index else 1
        super().save(*args, **kwargs)


def create_predefined_attributes():
    with transaction.atomic():
        for attribute in PREDEFINED_ATTRIBUTES:
            _, created = Attribute.objects.get_or_create(identifier=attribute['identifier'], defaults=attribute)
            if created:
                logger.info('Created attribute %s (%s)' % (attribute['name'], attribute['identifier']))
