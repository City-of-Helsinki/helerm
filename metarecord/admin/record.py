from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from metarecord.admin._common import StructuralElementAdmin
from metarecord.models.record import Record


@admin.register(Record)
class RecordAdmin(StructuralElementAdmin):
    list_display = ('get_classification_code', 'get_function_name', 'get_phase_name', 'get_action_name', 'get_name')
    list_filter = ('action__phase__function__classification__code',)
    search_fields = ('attributes',)

    fields = ('get_name', 'action', 'parent', 'attributes')
    ordering = ('action__phase__function__classification__code', 'index')
    raw_id_fields = ('action', 'parent')
    readonly_fields = ('get_name',)

    def get_classification_code(self, obj):
        return obj.action.phase.function.get_classification_code()
    get_classification_code.short_description = _('code')

    def get_function_name(self, obj):
        return obj.action.phase.function.get_name()
    get_function_name.short_description = _('function')

    def get_phase_name(self, obj):
        return obj.action.phase.get_name()
    get_phase_name.short_description = _('phase')

    def get_action_name(self, obj):
        return obj.action.get_name()
    get_action_name.short_description = _('action')

    def get_name(self, obj):
        return obj.get_name()
    get_name.short_description = _('name')
