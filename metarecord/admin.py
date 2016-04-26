from django import forms
from django.contrib import admin
from django.db import transaction
from django.db.utils import OperationalError

from .models import Action, Attribute, AttributeValue, Function, Phase, Record, RecordType, RecordAttachment


class ModelFormWithAttributes(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set initial values for the attribute fields
        for attribute in Attribute.objects.all():
            try:
                self.fields[attribute.name].initial = self.instance.attribute_values.get(attribute=attribute)
            except AttributeValue.DoesNotExist:
                pass


class StructuralElementAdmin(admin.ModelAdmin):
    exclude = ('attribute_values',)
    form = ModelFormWithAttributes

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Because Django executes ModelAdmin.__init__ when running manage.py migrate,
        # we need this check or else migrate fails if Attribute table hasn't been
        # created yet (empty db the most common case).
        try:
            attribute_list = list(Attribute.objects.values_list('name', 'is_free_text'))
        except OperationalError:
            return

        # Add dynamic attributes as ChoiceFields and CharFields to the form.
        # One known caveat in this method is that a restart is required for new
        # fields to show because this is run only at app startup.
        new_fields = []
        for name, is_free_text in attribute_list:
            if is_free_text:
                new_field = (
                    name,
                    forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 80}))
                )
            else:
                new_field = (
                    name,
                    forms.ModelChoiceField(
                        queryset=AttributeValue.objects.filter(attribute__name=name),
                        required=False
                    )
                )
            new_fields.append(new_field)
        self.form.base_fields.update(new_fields)

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        obj.save()

        # handle dynamic ManyToMany attribute saving
        for attribute in Attribute.objects.all():
            if attribute.name not in form.cleaned_data:
                continue

            value = form.cleaned_data.get(attribute.name)
            if value:
                obj.set_attribute_value(attribute, value)
            else:
                obj.remove_attribute_value(attribute)


class FunctionAdmin(StructuralElementAdmin):
    list_display = ('function_id', 'name')
    ordering = ('function_id',)
    exclude = ('attribute_values',)


class PhaseAdmin(StructuralElementAdmin):
    ordering = ('function__function_id', 'order')


class ActionAdmin(StructuralElementAdmin):
    ordering = ('phase__function__function_id', 'order')


class RecordAdmin(StructuralElementAdmin):
    ordering = ('action__phase__function__function_id', 'order')


class RecordAttachmentAdmin(StructuralElementAdmin):
    ordering = ('record__action__phase__function__function_id', 'order')


class AttributeValueInline(admin.StackedInline):
    model = AttributeValue
    extra = 0


class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    inlines = (AttributeValueInline,)

    class Meta:
        model = Attribute


admin.site.register(Function, FunctionAdmin)
admin.site.register(Phase, PhaseAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(RecordType)
admin.site.register(RecordAttachment, RecordAttachmentAdmin)
admin.site.register(Attribute, AttributeAdmin)
