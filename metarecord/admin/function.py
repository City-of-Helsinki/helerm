from django.contrib import admin
from django.db import transaction
from django.urls import path
from django.utils.translation import gettext_lazy as _

from metarecord.models.function import Function, MetadataVersion
from metarecord.views.admin import tos_import_view


class MetadataVersionInline(admin.TabularInline):
    can_delete = False
    verbose_name_plural = _("State history")

    model = MetadataVersion
    extra = 0
    readonly_fields = (
        "modified_at",
        "get_modified_by",
        "state",
        "valid_from",
        "valid_to",
    )
    exclude = ("modified_by", "_modified_by")

    @admin.display(description=_("modified by"))
    def get_modified_by(self, obj):
        return obj.get_modified_by_display()

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Function)
class FunctionAdmin(admin.ModelAdmin):
    list_display = ("get_classification_code", "get_name", "state", "version")
    list_filter = ("state", "classification__code")
    search_fields = ("classification__code", "classification__title", "uuid")

    ordering = ("classification__code", "version")
    fields = (
        "uuid",
        "state",
        "is_template",
        "error_count",
        "valid_from",
        "valid_to",
        "attributes",
    )
    readonly_fields = ("uuid",)
    inlines = (MetadataVersionInline,)

    @admin.display(description=_("classification code"))
    def get_classification_code(self, obj):
        return (
            obj.get_classification_code()
            if not obj.is_template
            else str(_("template")).upper()
        )

    @admin.display(description=_("name"))
    def get_name(self, obj):
        return obj.get_name()

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
            path(
                "import-tos/",
                self.admin_site.admin_view(self.tos_import_context),
                name="import-tos",
            )
        ] + urls
        return urls
