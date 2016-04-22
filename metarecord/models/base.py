import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(verbose_name=_('time of creation'), default=timezone.now, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('created by'),
                                   null=True, blank=True, related_name='%(class)s_created', editable=False)
    modified_at = models.DateTimeField(verbose_name=_('time of modification'), default=timezone.now, editable=False)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('modified by'),
                                    null=True, blank=True, related_name='%(class)s_modified', editable=False)

    class Meta:
        abstract = True


class Attribute(BaseModel):
    identifier = models.CharField(verbose_name=_('identifier'), max_length=64, unique=True, db_index=True)
    name = models.CharField(verbose_name=_('name'), max_length=256)

    class Meta:
        verbose_name = _('attribute')
        verbose_name_plural = _('attributes')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = self.pk
        super().save(*args, **kwargs)


class AttributeValue(BaseModel):
    attribute = models.ForeignKey(Attribute, verbose_name=_('attribute'), related_name='values')
    value = models.CharField(verbose_name=_('value'), max_length=256)

    class Meta:
        verbose_name = _('attribute value')
        verbose_name_plural = _('attribute values')

    def __str__(self):
        return '%s: %s' % (self.attribute, self.value)


class StructuralElement(BaseModel):
    order = models.PositiveSmallIntegerField(null=True, editable=False, db_index=True)
    attribute_values = models.ManyToManyField(AttributeValue, verbose_name=_('attribute values'))

    class Meta:
        abstract = True
        ordering = ['order']
