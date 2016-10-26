from django.contrib import admin

from .models import Action, Attribute, AttributeValue, Function, Phase, Record, RecordType
from .models.attribute import reload_attribute_schema


class StructuralElementAdmin(admin.ModelAdmin):
    exclude = ('attribute_values',)

    def get_form(self, request, obj=None, **kwargs):
        reload_attribute_schema()
        return super().get_form(request, obj, **kwargs)


class FunctionAdmin(StructuralElementAdmin):
    list_display = ('function_id', 'name')
    ordering = ('function_id',)
    exclude = ('attribute_values',)


class PhaseAdmin(StructuralElementAdmin):
    ordering = ('function__function_id', 'index')


class ActionAdmin(StructuralElementAdmin):
    ordering = ('phase__function__function_id', 'index')


class RecordAdmin(StructuralElementAdmin):
    ordering = ('action__phase__function__function_id', 'index')


class AttributeValueInline(admin.StackedInline):
    model = AttributeValue
    extra = 0


class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    inlines = (AttributeValueInline,)

    class Meta:
        model = Attribute


admin.site.register(Function, FunctionAdmin)
admin.site.register(Phase, PhaseAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(RecordType)
admin.site.register(Attribute, AttributeAdmin)
