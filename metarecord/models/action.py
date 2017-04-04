from django.db import models
from django.utils.translation import ugettext_lazy as _

from .phase import Phase
from .structural_element import StructuralElement


class Action(StructuralElement):
    phase = models.ForeignKey(Phase, verbose_name=_('phase'), related_name='actions')
    name = models.CharField(verbose_name=_('name'), max_length=256)

    # Action attribute validation rules, hardcoded at least for now
    _attribute_validations = {
        'allowed': (
            'ActionType', 'AdditionalInformation', 'InformationSystem', 'ProcessStatus'
        )
    }

    class Meta:
        verbose_name = _('action')
        verbose_name_plural = _('actions')
        ordering = ('phase', 'index')

    def __str__(self):
        return '%s | %s' % (self.phase, self.name)
