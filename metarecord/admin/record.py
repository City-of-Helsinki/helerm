from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from metarecord.models.record import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = (
        "get_classification_code",
        "get_function_name",
        "get_phase_name",
        "get_action_name",
        "get_name",
    )
    list_filter = ("action__phase__function__classification__code",)
    search_fields = ("attributes",)

    fields = ("get_name", "action", "parent", "attributes")
    ordering = ("action__phase__function__classification__code", "index")
    raw_id_fields = ("action", "parent")
    readonly_fields = ("get_name",)

    @admin.display(description=_("code"))
    def get_classification_code(self, obj):
        return obj.action.phase.function.get_classification_code()

    @admin.display(description=_("function"))
    def get_function_name(self, obj):
        return obj.action.phase.function.get_name()

    @admin.display(description=_("phase"))
    def get_phase_name(self, obj):
        return obj.action.phase.get_name()

    @admin.display(description=_("action"))
    def get_action_name(self, obj):
        return obj.action.get_name()

    @admin.display(description=_("name"))
    def get_name(self, obj):
        return obj.get_name()
