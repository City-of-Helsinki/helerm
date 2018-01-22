import json

from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin
from django.contrib.postgres.forms.hstore import HStoreField
from django.db import transaction
from django.urls import path
from django.utils.translation import ugettext_lazy as _

from .models import (
    Action, Attribute, AttributeGroup, AttributeValue, Classification, Function, MetadataVersion, Phase, Record
)
from .views.admin import tos_import_view


# disable non ascii char escaping in hstore field
class UTF8HStoreField(HStoreField):
    def prepare_value(self, value):
        if isinstance(value, dict):
            return json.dumps(value, ensure_ascii=False)
        return value


class StructuralElementAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        kwargs['field_classes'] = {'attributes': UTF8HStoreField}
        return super().get_form(request, obj, **kwargs)


class MetadataVersionInline(admin.TabularInline):
    can_delete = False
    verbose_name_plural = _('State history')

    model = MetadataVersion
    extra = 0
    readonly_fields = ('modified_at', 'modified_by', 'state', 'valid_from', 'valid_to')

    def has_add_permission(self, request):
        return False


class FunctionAdmin(StructuralElementAdmin):
    list_display = ('get_classification_code', 'get_name', 'state', 'version')
    list_filter = ('state',)
    search_fields = ('classification__code', 'classification__title')

    ordering = ('classification__code', 'version')
    fields = ('state', 'is_template', 'error_count', 'valid_from', 'valid_to', 'attributes')
    inlines = (MetadataVersionInline,)

    def get_classification_code(self, obj):
        return obj.get_classification_code() if not obj.is_template else str(_('template')).upper()
    get_classification_code.short_description = _('classification code')

    def get_name(self, obj):
        return obj.get_name()
    get_name.short_description = _('name')

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.pk is None:
            obj.create_metadata_version()

    def get_urls(self):
        urls = super().get_urls()
        urls = [
            path('import-tos/', self.admin_site.admin_view(tos_import_view), name='import-tos')
        ] + urls
        return urls


class PhaseAdmin(StructuralElementAdmin):
    fields = ('name', 'function', 'attributes')
    ordering = ('function__classification__code', 'index')
    raw_id_fields = ('function',)
    readonly_fields = ('name',)
    search_fields = ('attributes',)

    def name(self, obj):
        return obj.get_name()
    name.short_description = _('name')


class ActionAdmin(StructuralElementAdmin):
    fields = ('name', 'phase', 'attributes')
    ordering = ('phase__function__classification__code', 'index')
    raw_id_fields = ('phase',)
    readonly_fields = ('name',)
    search_fields = ('attributes',)

    def name(self, obj):
        return obj.get_name()
    name.short_description = _('name')


class RecordAdmin(StructuralElementAdmin):
    fields = ('name', 'action', 'parent', 'attributes')
    ordering = ('action__phase__function__classification__code', 'index')
    raw_id_fields = ('action', 'parent')
    readonly_fields = ('name',)
    search_fields = ('attributes',)

    def name(self, obj):
        return obj.get_name()
    name.short_description = _('name')


class AttributeValueInline(SortableInlineAdminMixin, admin.TabularInline):
    model = AttributeValue
    extra = 0


class AttributeAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'group')
    inlines = (AttributeValueInline,)
    exclude = ('index',)

    class Meta:
        model = Attribute


class AttributeGroupAdmin(admin.ModelAdmin):
    model = AttributeGroup


class ClassificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'function_allowed')
    ordering = ('code',)


admin.site.register(Function, FunctionAdmin)
admin.site.register(Phase, PhaseAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(AttributeGroup, AttributeGroupAdmin)
admin.site.register(Classification, ClassificationAdmin)
