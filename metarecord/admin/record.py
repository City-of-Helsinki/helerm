from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from metarecord.admin._common import StructuralElementAdmin
from metarecord.models.record import Record


@admin.register(Record)
class RecordAdmin(StructuralElementAdmin):
    fields = ('name', 'action', 'parent', 'attributes')
    ordering = ('action__phase__function__classification__code', 'index')
    raw_id_fields = ('action', 'parent')
    readonly_fields = ('name',)
    search_fields = ('attributes',)

    def name(self, obj):
        return obj.get_name()
    name.short_description = _('name')
