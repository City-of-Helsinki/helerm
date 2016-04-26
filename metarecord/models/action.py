from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import StructuralElement
from .phase import Phase


class Action(StructuralElement):
    phase = models.ForeignKey(Phase, verbose_name=_('phase'), related_name='actions')
    name = models.CharField(verbose_name=_('name'), max_length=256)

    class Meta:
        verbose_name = _('action')
        verbose_name_plural = _('actions')

    def __str__(self):
        return '%s | %s' % (self.phase, self.name)
