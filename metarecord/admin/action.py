from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from metarecord.admin._common import StructuralElementAdmin
from metarecord.models.action import Action


@admin.register(Action)
class ActionAdmin(StructuralElementAdmin):
    fields = ('name', 'phase', 'attributes')
    ordering = ('phase__function__classification__code', 'index')
    raw_id_fields = ('phase',)
    readonly_fields = ('name',)
    search_fields = ('attributes',)

    def name(self, obj):
        return obj.get_name()
    name.short_description = _('name')
