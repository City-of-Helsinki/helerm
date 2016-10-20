import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_hstore import hstore


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(verbose_name=_('time of creation'), default=timezone.now, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('created by'),
                                   null=True, blank=True, related_name='%(class)s_created', editable=False)
    modified_at = models.DateTimeField(verbose_name=_('time of modification'), default=timezone.now, editable=False)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('modified by'),
                                    null=True, blank=True, related_name='%(class)s_modified', editable=False)

    class Meta:
        abstract = True


class StructuralElement(BaseModel):
    index = models.PositiveSmallIntegerField(null=True, editable=False, db_index=True)
    attributes = hstore.DictionaryField(blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ('index',)
