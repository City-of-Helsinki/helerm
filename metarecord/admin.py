from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from adminsortable2.admin import SortableAdminMixin

from .models import Action, Attribute, AttributeValue, Function, Phase, Record
from .models.structural_element import use_attribute_schema


class StructuralElementAdmin(admin.ModelAdmin):
    exclude = ('attribute_values',)

    @use_attribute_schema()
    def changeform_view(self, *args, **kwargs):
        return super().changeform_view(*args, **kwargs)

    def get_fieldsets(self, request, obj=None):
        all_fields = self.get_fields(request, obj)
        attribute_fields = Attribute.objects.values_list('identifier', flat=True)
        normal_fields = [field for field in all_fields if field not in attribute_fields]

        return (
            (None, {
                'fields': normal_fields,
            }),
            (_('attributes'), {
                'fields': attribute_fields,
            }),
        )


class FunctionAdmin(StructuralElementAdmin):
    list_display = ('get_function_id', 'name', 'state', 'version')
    ordering = ('function_id', 'version')
    fields = ('parent', 'function_id', 'name', 'state', 'is_template', 'error_count')

    def get_function_id(self, obj):
        return obj.function_id if not obj.is_template else '* %s *' % _('template').upper()
    get_function_id.short_description = _('function ID')


class PhaseAdmin(StructuralElementAdmin):
    ordering = ('function__function_id', 'index')


class ActionAdmin(StructuralElementAdmin):
    ordering = ('phase__function__function_id', 'index')


class RecordAdmin(StructuralElementAdmin):
    ordering = ('action__phase__function__function_id', 'index')


class AttributeValueInline(admin.StackedInline):
    model = AttributeValue
    extra = 0


class AttributeAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name',)
    inlines = (AttributeValueInline,)
    exclude = ('index',)

    class Meta:
        model = Attribute


admin.site.register(Function, FunctionAdmin)
admin.site.register(Phase, PhaseAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Attribute, AttributeAdmin)
