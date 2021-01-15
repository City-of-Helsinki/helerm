from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from metarecord.models.action import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('get_classification_code', 'get_function_name', 'get_phase_name', 'get_name')
    list_filter = ('phase__function__classification__code',)
    search_fields = ('attributes',)

    fields = ('get_name', 'phase', 'attributes')
    ordering = ('phase__function__classification__code', 'index')
    raw_id_fields = ('phase',)
    readonly_fields = ('get_name',)

    def get_classification_code(self, obj):
        return obj.phase.function.get_classification_code()
    get_classification_code.short_description = _('code')

    def get_function_name(self, obj):
        return obj.phase.function.get_name()
    get_function_name.short_description = _('function')

    def get_phase_name(self, obj):
        return obj.phase.get_name()
    get_phase_name.short_description = _('phase')

    def get_name(self, obj):
        return obj.get_name()
    get_name.short_description = _('name')
