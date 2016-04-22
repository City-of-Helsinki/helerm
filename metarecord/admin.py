from django import forms
from django.contrib import admin

from .models import Action, Attribute, AttributeValue, Function, Phase, Record, RecordType


class ModelFormWithAttributes(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set initial values for the attribute fields
        for name in Attribute.objects.values_list('name', flat=True):
            try:
                self.fields[name].initial = self.instance.attribute_values.get(attribute__name=name)
            except AttributeValue.DoesNotExist:
                pass


class StructuralElementAdmin(admin.ModelAdmin):
    exclude = ('attribute_values',)
    form = ModelFormWithAttributes

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add dynamic attributes as ChoiceFields to the form.
        # One known caveat in this method is that a restart is required for new fields to show
        # because this is run only at app startup.
        new_fields = []
        for name in Attribute.objects.values_list('name', flat=True):
            new_fields.append((
                name,
                forms.ModelChoiceField(
                    queryset=AttributeValue.objects.filter(attribute__name=name),
                    required=False)
                )
            )
        self.form.base_fields.update(new_fields)

    def save_model(self, request, obj, form, change):
        obj.save()

        # Handle dynamic ManyToMany attributes
        for name in Attribute.objects.values_list('name', flat=True):
            value = form.cleaned_data.get(name)
            if value:
                obj.attribute_values.add(form.cleaned_data.get(name))
            else:
                try:
                    attribute_value = obj.attribute_values.get(attribute__name=name)
                    obj.attribute_values.remove(attribute_value)
                except AttributeValue.DoesNotExist:
                    pass


class FunctionAdmin(StructuralElementAdmin):
    list_display = ('function_id', 'name')
    ordering = ('function_id',)
    exclude = ('attribute_values',)


class PhaseAdmin(StructuralElementAdmin):
    pass


class ActionAdmin(StructuralElementAdmin):
    pass


class RecordAdmin(StructuralElementAdmin):
    pass


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
admin.site.register(Attribute, AttributeAdmin)
