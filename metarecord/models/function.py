from django.db import models
from django.utils.translation import ugettext_lazy as _

from .attributes import AllAttributesModel


class Function(AllAttributesModel):
    function_id = models.CharField(verbose_name=_('function ID'), max_length=16)
    parent = models.ForeignKey('self', verbose_name=_('parent'), blank=True, null=True)
    name = models.CharField(verbose_name=_('name'), max_length=256)

    class Meta:
        verbose_name = _('function')
        verbose_name_plural = _('functions')

    def __str__(self):
        return self.name
