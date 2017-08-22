import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import TimeStampedModel


class Classification(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    parent = models.ForeignKey('self', verbose_name=_('parent'), related_name='children', blank=True, null=True)
    code = models.CharField(verbose_name=_('code'), max_length=16, db_index=True)
    title = models.CharField(verbose_name=_('title'), max_length=256)
    description = models.TextField(verbose_name=_('description'), blank=True)
    description_internal = models.TextField(verbose_name=_('description internal'), blank=True)

    class Meta:
        verbose_name = _('classification')
        verbose_name_plural = _('classifications')

    def __str__(self):
        return self.code
