from django.db import models
from django.utils.translation import ugettext_lazy as _

from .action import Action
from .attributes import AllAttributesModel


class Record(AllAttributesModel):
    action = models.ForeignKey(Action, verbose_name=_('action'), related_name='records')
    type = models.CharField(verbose_name=_('type'), max_length=64)
    type_specifier = models.CharField(verbose_name=_('type specifier'), max_length=256, blank=True)

    class Meta:
        verbose_name = _('record')
        verbose_name_plural = _('records')

    def __str__(self):
        return '%s/%s' % (self.action, self.name)
