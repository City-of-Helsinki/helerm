from django.contrib import admin
from django.db import transaction
from django.urls import path
from django.utils.translation import ugettext_lazy as _

from metarecord.admin._common import StructuralElementAdmin
from metarecord.models.function import Function, MetadataVersion
from metarecord.views.admin import tos_import_view


class MetadataVersionInline(admin.TabularInline):
    can_delete = False
    verbose_name_plural = _('State history')

    model = MetadataVersion
    extra = 0
    readonly_fields = ('modified_at', 'modified_by', 'state', 'valid_from', 'valid_to')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Function)
class FunctionAdmin(StructuralElementAdmin):
    list_display = ('get_classification_code', 'get_name', 'state', 'version')
    list_filter = ('state', 'classification__code')
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

    def tos_import_context(self, request):
        context = dict(
           self.admin_site.each_context(request),
        )
        return tos_import_view(request, context)

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.pk is None:
            obj.create_metadata_version()

    def get_urls(self):
        urls = super().get_urls()
        urls = [
            path('import-tos/', self.admin_site.admin_view(self.tos_import_context), name='import-tos')
        ] + urls
        return urls
