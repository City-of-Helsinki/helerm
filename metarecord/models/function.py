from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import StructuralElement


class Function(StructuralElement):
    function_id = models.CharField(verbose_name=_('function ID'), max_length=16, unique=True, db_index=True)
    parent = models.ForeignKey('self', verbose_name=_('parent'), blank=True, null=True)
    name = models.CharField(verbose_name=_('name'), max_length=256)
    error_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _('function')
        verbose_name_plural = _('functions')

    def __str__(self):
        return '%s %s' % (self.function_id, self.name)
