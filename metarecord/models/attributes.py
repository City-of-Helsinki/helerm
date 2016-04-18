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


class RetentionCalculationBasis(AttributeValueString):
    class Meta:
        verbose_name = _('retention calculation basis')
        verbose_name_plural = _('retention calculation bases')


class PaperRecordRetentionOrder(AttributeValueString):
    class Meta:
        verbose_name = _('paper record retention order')
        verbose_name_plural = _('paper record retention orders')


class InformationSystem(AttributeValueString):
    class Meta:
        verbose_name = _('information system')
        verbose_name_plural = _('information systems')


class PaperRecordArchiveRetentionPeriod(AttributeValueString):
    class Meta:
        verbose_name = _('paper record archive retention period')
        verbose_name_plural = _('paper record archive retention periods')


class PaperRecordWorkplaceRetentionPeriod(AttributeValueString):
    class Meta:
        verbose_name = _('paper record workplace retention period')
        verbose_name_plural = _('paper record workplace retention periods')


class SecurityPeriodCalculationBasis(AttributeValueString):
    class Meta:
        verbose_name = _('security period calculation basis')
        verbose_name_plural = _('security period calculation bases')


class PaperRecordRetentionLocation(AttributeValueString):
    class Meta:
        verbose_name = _('paper record retention location')
        verbose_name_plural = _('paper record retention locations')


class PaperRecordRetentionResponsiblePerson(AttributeValueString):
    class Meta:
        verbose_name = _('paper record retention responsible person')
        verbose_name_plural = _('paper record retention responsible persons')


class AdditionalInformation(AttributeValueString):
    class Meta:
        verbose_name = _('additional information')
        verbose_name_plural = _('additional information')


class CommonAttributesModel(BaseModel):
    """Base class containing all common attributes."""

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
    retention_calculation_basis = models.ForeignKey(RetentionCalculationBasis,
                                                    verbose_name=_('retention calculation basis'),
                                                    related_name='%(class)ss', blank=True, null=True)
    information_system = models.ForeignKey(InformationSystem, verbose_name=_('information system'),
                                           related_name='%(class)ss', blank=True, null=True)
    security_period_calculation_basis = models.ForeignKey(SecurityPeriodCalculationBasis,
                                                          verbose_name=_('security period calculation basis'),
                                                          related_name='%(class)ss', blank=True, null=True)
    additional_information = models.ForeignKey(AdditionalInformation, verbose_name=_('additional information'),
                                               related_name='%(class)ss', blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ['order']
