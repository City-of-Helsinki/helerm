import uuid
from collections import Iterable

from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

from .base import TimeStampedModel


class Classification(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    parent = models.ForeignKey(
        'self', verbose_name=_('parent'), related_name='children', blank=True, null=True, on_delete=models.SET_NULL
    )
    code = models.CharField(verbose_name=_('code'), max_length=16, db_index=True)
    title = models.CharField(verbose_name=_('title'), max_length=256)
    description = models.TextField(verbose_name=_('description'), blank=True)
    description_internal = models.TextField(verbose_name=_('description internal'), blank=True)
    related_classification = models.TextField(verbose_name=_('related classification'), blank=True)
    additional_information = models.TextField(verbose_name=_('additional information'), blank=True)
    function_allowed = models.BooleanField(verbose_name=_('function allowed'), default=False)

    class Meta:
        verbose_name = _('classification')
        verbose_name_plural = _('classifications')

    def __str__(self):
        return self.code


@transaction.atomic
def update_function_allowed(classifications):
    if not isinstance(classifications, Iterable):
        classifications = (classifications,)

    for classification in classifications:
        classification.function_allowed = not classification.children.exists()
        classification.save(update_fields=('function_allowed',))
