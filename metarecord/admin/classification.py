from django.contrib import admin
from django.http import (
    HttpResponseForbidden,
    HttpResponseNotAllowed,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404
from django.urls import path, reverse

from metarecord.models.classification import Classification


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    change_form_template = "admin/metarecord/classification/change_form.html"
    list_display = ("code", "version", "state", "title", "function_allowed")
    search_fields = ("code", "title")
    ordering = ("code", "version")
    list_filter = ("state", "code")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/new-version/",
                self.admin_site.admin_view(self.create_new_version_view),
                name="metarecord_classification_create-new-version",
            ),
        ]
        return custom_urls + urls

    def create_new_version_view(self, request, object_id):
        """
        Create new classification draft version with the information
        carried over from the latest version
        """
        if request.method != "POST":
            return HttpResponseNotAllowed(permitted_methods="POST")

        if not request.user.has_perm(Classification.CAN_EDIT):
            return HttpResponseForbidden()

        classification = get_object_or_404(Classification, pk=object_id)

        latest_version = Classification.objects.latest_version().get(
            uuid=classification.uuid
        )
        latest_version.pk = None  # New version will be created if pk is none
        latest_version.state = Classification.DRAFT
        latest_version.save()

        return HttpResponseRedirect(
            reverse(
                "admin:metarecord_classification_change",
                kwargs={"object_id": latest_version.pk},
            )
        )
