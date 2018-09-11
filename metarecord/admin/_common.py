from django.contrib import admin

from metarecord.forms import UTF8HStoreField


class StructuralElementAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        kwargs['field_classes'] = {'attributes': UTF8HStoreField}
        return super().get_form(request, obj, **kwargs)
