import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(verbose_name=_('time of creation'), auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(verbose_name=_('time of modification'), auto_now=True, editable=False)

    class Meta:
        abstract = True


class UUIDPrimaryKeyModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
