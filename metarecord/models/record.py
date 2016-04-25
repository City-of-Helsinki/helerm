from django.db import models
from django.utils.translation import ugettext_lazy as _

from .action import Action
from .base import BaseModel, StructuralElement


class RecordType(BaseModel):
    value = models.CharField(verbose_name=_('name'), max_length=256)

    class Meta:
        verbose_name = _('record type')
        verbose_name_plural = _('record type')

    def __str__(self):
        return self.value


class Record(StructuralElement):
    action = models.ForeignKey(Action, verbose_name=_('action'), related_name='records')
    name = models.CharField(verbose_name=_('type specifier'), max_length=256)
    type = models.ForeignKey(RecordType, verbose_name=_('type'))

    class Meta:
        verbose_name = _('record')
        verbose_name_plural = _('records')

    def __str__(self):
        return '%s/%s' % (self.action, self.type)
