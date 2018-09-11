from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from metarecord.admin._common import StructuralElementAdmin
from metarecord.models.phase import Phase


@admin.register(Phase)
class PhaseAdmin(StructuralElementAdmin):
    fields = ('name', 'function', 'attributes')
    ordering = ('function__classification__code', 'index')
    raw_id_fields = ('function',)
    readonly_fields = ('name',)
    search_fields = ('attributes',)

    def name(self, obj):
        return obj.get_name()
    name.short_description = _('name')
