from django.contrib import admin

from ..models.bulk_update import BulkUpdate


@admin.register(BulkUpdate)
class BulkUpdateAdmin(admin.ModelAdmin):
    pass
