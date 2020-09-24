from django.contrib import admin

from metarecord.models.classification import Classification


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'version', 'state', 'title', 'function_allowed')
    search_fields = ('code', 'title')
    ordering = ('code', 'version')
