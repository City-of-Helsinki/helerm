import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(verbose_name=_('time of creation'), default=timezone.now, editable=False)
    modified_at = models.DateTimeField(verbose_name=_('time of modification'), default=timezone.now, editable=False)

    class Meta:
        abstract = True


class UUIDPrimaryKeyModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
