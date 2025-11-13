from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from metarecord.models.phase import Phase


@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ("get_classification_code", "get_function_name", "get_name")
    list_filter = ("function__classification__code",)
    search_fields = ("attributes", "uuid")

    fields = ("uuid", "get_name", "function", "attributes")
    ordering = ("function__classification__code", "index")
    raw_id_fields = ("function",)
    readonly_fields = ("get_name", "uuid")

    @admin.display(description=_("code"))
    def get_classification_code(self, obj):
        return obj.function.get_classification_code()

    @admin.display(description=_("function"))
    def get_function_name(self, obj):
        return obj.function.get_name()

    @admin.display(description=_("name"))
    def get_name(self, obj):
        return obj.get_name()
