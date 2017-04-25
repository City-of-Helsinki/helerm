from django.contrib import admin
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from adminsortable2.admin import SortableAdminMixin

from .models import Action, Attribute, AttributeGroup, AttributeValue, Function, Phase, Record, MetadataVersion


class MetadataVersionInline(admin.TabularInline):
    can_delete = False
    verbose_name_plural = _('State history')

    model = MetadataVersion
    extra = 0
    readonly_fields = ('modified_at', 'modified_by', 'state', 'valid_from', 'valid_to')

    def has_add_permission(self, request):
        return False


class FunctionAdmin(admin.ModelAdmin):
    list_display = ('get_function_id', 'name', 'state', 'version')
    list_filter = ('state',)
    search_fields = ('function_id', 'name')

    ordering = ('function_id', 'version')
    fields = (
        'parent', 'function_id', 'state', 'is_template', 'error_count', 'valid_from', 'valid_to', 'attributes'
    )
    inlines = (MetadataVersionInline,)

    def get_function_id(self, obj):
        return obj.function_id if not obj.is_template else '* %s *' % _('template').upper()
    get_function_id.short_description = _('function ID')

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.pk is None:
            obj.create_metadata_version()


class PhaseAdmin(admin.ModelAdmin):
    fields = ('name', 'function', 'attributes')
    ordering = ('function__function_id', 'index')
    raw_id_fields = ('function',)
    readonly_fields = ('name',)
    search_fields = ('attributes',)

    def name(self, obj):
        return obj.get_name()
    name.short_description = _('name')


class ActionAdmin(admin.ModelAdmin):
    fields = ('name', 'phase', 'attributes')
    ordering = ('phase__function__function_id', 'index')
    raw_id_fields = ('phase',)
    readonly_fields = ('name',)
    search_fields = ('attributes',)

    def name(self, obj):
        return obj.get_name()
    name.short_description = _('name')


class RecordAdmin(admin.ModelAdmin):
    fields = ('name', 'action', 'parent', 'attributes')
    ordering = ('action__phase__function__function_id', 'index')
    raw_id_fields = ('action', 'parent')
    readonly_fields = ('name',)
    search_fields = ('attributes',)

    def name(self, obj):
        return obj.get_name()
    name.short_description = _('name')


class AttributeValueInline(admin.StackedInline):
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


admin.site.register(Function, FunctionAdmin)
admin.site.register(Phase, PhaseAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(AttributeGroup, AttributeGroupAdmin)
