from django.db import models
from django.utils.translation import ugettext_lazy as _

from .phase import Phase
from .structural_element import StructuralElement


class Action(StructuralElement):
    phase = models.ForeignKey(Phase, verbose_name=_('phase'), related_name='actions', on_delete=models.CASCADE)

    # Action attribute validation rules, hardcoded at least for now
    _attribute_validations = {
        'allowed': (
            'ActionType', 'AdditionalInformation', 'InformationSystem', 'ProcessStatus', 'TypeSpecifier'
        ),
        'multivalued': (
            'InformationSystem',
        ),
        'allow_values_outside_choices': (
            'InformationSystem',
        ),
    }

    class Meta:
        verbose_name = _('action')
        verbose_name_plural = _('actions')
        ordering = ('phase', 'index')

    def __str__(self):
        return '%s | %s' % (self.phase, self.get_name() or '-')

    def get_name(self):
        type_specifier = self.attributes.get('TypeSpecifier')
        if type_specifier:
            return type_specifier
        return self.attributes.get('ActionType')
