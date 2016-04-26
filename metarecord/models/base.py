import uuid

from django.conf import settings
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


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


class Attribute(BaseModel):
    identifier = models.CharField(verbose_name=_('identifier'), max_length=64, unique=True, db_index=True)
    name = models.CharField(verbose_name=_('name'), max_length=256)
    is_free_text = models.BooleanField(verbose_name=_('is free text'), default=False)

    class Meta:
        verbose_name = _('attribute')
        verbose_name_plural = _('attributes')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = self.pk
        super().save(*args, **kwargs)

    @staticmethod
    def get_attribute_obj(attribute):
        if isinstance(attribute, Attribute):
            return attribute
        try:
            return Attribute.objects.get(identifier=attribute)
        except Attribute.DoesNotExist:
            raise Exception('Attribute %s does not exist.' % attribute)


class AttributeValue(BaseModel):
    attribute = models.ForeignKey(Attribute, verbose_name=_('attribute'), related_name='values')
    value = models.CharField(verbose_name=_('value'), max_length=1024)

    class Meta:
        verbose_name = _('attribute value')
        verbose_name_plural = _('attribute values')

    def __str__(self):
        return self.value


class StructuralElement(BaseModel):
    order = models.PositiveSmallIntegerField(null=True, editable=False, db_index=True)
    attribute_values = models.ManyToManyField(AttributeValue, verbose_name=_('attribute values'))

    class Meta:
        abstract = True
        ordering = ['order']

    @transaction.atomic
    def set_attribute_value(self, attribute, value):
        """
        Set a ManyToMany attribute's value.

        :param attribute: Attribute object or identifier
        :type attribute: Attribute or str
        :type value: str
        """
        print('set attr value attr %s value %s' % (attribute, value))
        attribute_obj = Attribute.get_attribute_obj(attribute)
        self.remove_attribute_value(attribute)

        if attribute_obj.is_free_text:
            value_obj = AttributeValue.objects.create(attribute=attribute_obj, value=value)
        else:
            value_obj = AttributeValue.objects.get(attribute=attribute_obj, value=value)
        print('value obj %s' % value_obj)
        self.attribute_values.add(value_obj)

    def remove_attribute_value(self, attribute):
        """
        Remove a ManyToMany attribute's value.

        :param attribute: Attribute object or identifier
        :type attribute: Attribute or str
        """
        attribute_obj = Attribute.get_attribute_obj(attribute)
        try:
            attribute_value = self.attribute_values.get(attribute=attribute_obj)
        except AttributeValue.DoesNotExist:
            return

        if attribute_obj.is_free_text:
            attribute_value.delete()
        else:
            self.attribute_values.remove(attribute_value)

    def get_attribute_value(self, attribute):
        """
        Get a ManyToMany attribute's value.

        :param attribute: Attribute object or identifier
        :type attribute: Attribute or str
        :rtype: str
        """
        attribute_obj = Attribute.get_attribute_obj(attribute)
        try:
            value_obj = self.attribute_values.get(attribute=attribute_obj)
        except AttributeValue.DoesNotExist:
            value_obj = None

        return value_obj.value if value_obj else None
