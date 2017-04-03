from django.db import models
from django.utils.translation import ugettext_lazy as _

from .function import Function
from .structural_element import StructuralElement


class Phase(StructuralElement):
    function = models.ForeignKey(Function, verbose_name=_('function'), related_name='phases')
    name = models.CharField(verbose_name=_('name'), max_length=256)

    # Phase attribute validation rules, hardcoded at least for now
    _attribute_validations = {
        'allowed': (
            'AdditionalInformation', 'InformationSystem'
        )
    }

    class Meta:
        verbose_name = _('phase')
        verbose_name_plural = _('phases')
        ordering = ('function', 'index')

    def __str__(self):
        return '%s | %s' % (self.function, self.name)
