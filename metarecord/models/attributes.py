from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import BaseModel


class BaseAttributeValue(BaseModel):
    @classmethod
    def get_referencing_field_name(self, model):
        for field in model._meta.get_fields():
            if field.related_model == self:
                return field.name
        return None

    def __str__(self):
        return str(self.value)

    class Meta:
        abstract = True


class AttributeValueString(BaseAttributeValue):
    """Base class for attribute values of type string."""
    value = models.CharField(verbose_name=_('value'), max_length=256)

    class Meta:
        abstract = True


class AttributeValueInteger(BaseAttributeValue):
    """Base class for attribute values of type integer."""
    value = models.IntegerField(verbose_name=_('value'))

    class Meta:
        abstract = True


class PublicityClass(AttributeValueString):
    class Meta:
        verbose_name = _('publicity class')
        verbose_name_plural = _('publicity classes')


class SecurityPeriod(AttributeValueInteger):
    class Meta:
        verbose_name = _('security period')
        verbose_name_plural = _('security periods')


class SecurityReason(AttributeValueString):
    class Meta:
        verbose_name = _('security reasons')
        verbose_name_plural = _('security reasons')


class PersonalData(AttributeValueString):
    class Meta:
        verbose_name = _('personal data')
        verbose_name_plural = _('personal data')


class SocialSecurityNumber(AttributeValueString):
    class Meta:
        verbose_name = _('social security number')
        verbose_name_plural = _('social security numbers')


class RetentionPeriod(AttributeValueInteger):
    class Meta:
        verbose_name = _('retention period')
        verbose_name_plural = _('retention periods')


class RetentionReason(AttributeValueString):
    class Meta:
        verbose_name = _('retention reason')
        verbose_name_plural = _('retention reasons')


class ProtectionClass(AttributeValueString):
    class Meta:
        verbose_name = _('protection class')
        verbose_name_plural = _('protection classes')


class RecordType(AttributeValueString):
    class Meta:
        verbose_name = _('record type')
        verbose_name_plural = _('record type')


class AllAttributesModel(BaseModel):
    """Base class containing all the attributes."""

    order = models.PositiveSmallIntegerField(null=True, editable=False, db_index=True)

    publicity_class = models.ForeignKey(PublicityClass, verbose_name=_('publicity class'), related_name='%(class)ss',
                                        blank=True, null=True)
    security_period = models.ForeignKey(SecurityPeriod, verbose_name=_('security period'), related_name='%(class)ss',
                                        blank=True, null=True)
    security_reason = models.ForeignKey(SecurityReason, verbose_name=_('security reason'), related_name='%(class)ss',
                                        blank=True, null=True)
    personal_data = models.ForeignKey(PersonalData, verbose_name=_('personal data'), related_name='%(class)ss',
                                      blank=True, null=True)
    social_security_number = models.ForeignKey(SocialSecurityNumber, verbose_name=_('social security number'),
                                               related_name='%(class)ss', blank=True, null=True)
    retention_period = models.ForeignKey(RetentionPeriod, verbose_name=_('retention period'), related_name='%(class)ss',
                                         blank=True, null=True)
    retention_reason = models.ForeignKey(RetentionReason, verbose_name=_('retention reason'), related_name='%(class)ss',
                                         blank=True, null=True)
    protection_class = models.ForeignKey(ProtectionClass, verbose_name=_('protection class'), related_name='%(class)ss',
                                         blank=True, null=True)
    # TODO Salassapitoajan laskentaperuste
    # TODO Säilytysajan laskentaperuste
    # TODO Lisätietoja
    # TODO Paperiasiakirjojen säilytysjärjestys
    # TODO Paperiasiakirjojen säilytysaika työpisteessä
    # TODO Paperiasiakirjojen säilytysaika arkistossa = paperiasiakirjojen kokonaissäilytysaika
    # TODO Paperiasiakirjojen säilytyspaikka
    # TODO Paperiasiakirjojen säilytyksen vastuuhenkilö (työntekijän nimike)

    class Meta:
        abstract = True
        ordering = ['order']
