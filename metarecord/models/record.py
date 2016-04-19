from django.db import models
from django.utils.translation import ugettext_lazy as _

from .action import Action
from .attributes import (CommonAttributesModel, PaperRecordArchiveRetentionPeriod, PaperRecordRetentionOrder,
                         PaperRecordWorkplaceRetentionPeriod, RecordType)


class Record(CommonAttributesModel):
    action = models.ForeignKey(Action, verbose_name=_('action'), related_name='records')
    name = models.CharField(verbose_name=_('type specifier'), max_length=256)
    type = models.ForeignKey(RecordType, verbose_name=_('type'))

    paper_record_retention_order = models.ForeignKey(
        PaperRecordRetentionOrder,
        verbose_name=_('paper record retention order'),
        related_name='%(class)ss',
        blank=True, null=True
    )
    paper_record_archive_retention_period = models.ForeignKey(
        PaperRecordArchiveRetentionPeriod,
        verbose_name=_('paper record archive retention period'),
        related_name='%(class)ss',
        blank=True, null=True
    )
    paper_record_workplace_retention_period = models.ForeignKey(
        PaperRecordWorkplaceRetentionPeriod,
        verbose_name=_('paper record workplace retention period'),
        related_name='%(class)ss',
        blank=True, null=True
    )
    paper_record_retention_location = models.CharField(verbose_name=_('paper record retention location'),
                                                       max_length=256, blank=True, null=True)
    paper_record_retention_responsible_person = models.CharField(
        verbose_name=_('paper record retention responsible person'),
        max_length=256, blank=True, null=True
    )

    class Meta:
        verbose_name = _('record')
        verbose_name_plural = _('records')

    def __str__(self):
        return '%s/%s' % (self.action, self.type)
