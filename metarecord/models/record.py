from django.db import models
from django.utils.translation import ugettext_lazy as _

from .action import Action
from .attributes import AllAttributesModel, RecordType


class Record(AllAttributesModel):
    action = models.ForeignKey(Action, verbose_name=_('action'), related_name='records')
    name = models.CharField(verbose_name=_('type'), max_length=256)
    type = models.ForeignKey(RecordType)

    class Meta:
        verbose_name = _('record')
        verbose_name_plural = _('records')

    def __str__(self):
        return '%s/%s' % (self.action, self.type)
