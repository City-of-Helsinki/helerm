from django.db import models
from django.utils.translation import ugettext_lazy as _

from .attributes import AllAttributesModel
from .function import Function


class Phase(AllAttributesModel):
    function = models.ForeignKey(Function, verbose_name=_('function'), related_name='phases')
    name = models.CharField(verbose_name=_('name'), max_length=256)

    class Meta:
        verbose_name = _('phase')
        verbose_name_plural = _('phases')

    def __str__(self):
        return '%s/%s' % (self.function, self.name)
