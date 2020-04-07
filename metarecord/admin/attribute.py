from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin

from metarecord.models.attribute import Attribute, AttributeGroup, AttributeValue


class AttributeValueInline(SortableInlineAdminMixin, admin.TabularInline):
    model = AttributeValue
    extra = 0


@admin.register(Attribute)
class AttributeAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'group')
    list_filter = ('group',)
    search_fields = ('name',)

    inlines = (AttributeValueInline,)
    exclude = ('index',)

    class Meta:
        model = Attribute


@admin.register(AttributeGroup)
class AttributeGroupAdmin(admin.ModelAdmin):
    model = AttributeGroup
