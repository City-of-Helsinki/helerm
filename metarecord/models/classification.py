import uuid
from collections.abc import Iterable

from django.contrib.auth import get_user_model
from django.db import connection, models, transaction
from django.utils.translation import gettext_lazy as _

from .base import TimeStampedModel


class ClassificationQuerySet(models.QuerySet):
    def latest_version(self):
        return self.order_by("code", "-version").distinct("code")

    def latest_approved(self):
        return self.filter(state=Classification.APPROVED).latest_version()

    def filter_for_user(self, user):
        if not user.is_authenticated:
            return self.filter(state=Classification.APPROVED)
        return self

    def previous_versions(self, classification):
        return self.filter(version__lt=classification.version, uuid=classification.uuid)

    def non_approved(self):
        return self.exclude(state=Classification.APPROVED)


class Classification(TimeStampedModel):
    DRAFT = "draft"
    SENT_FOR_REVIEW = "sent_for_review"
    WAITING_FOR_APPROVAL = "waiting_for_approval"
    APPROVED = "approved"

    STATE_CHOICES = (
        (DRAFT, _("Draft")),
        (SENT_FOR_REVIEW, _("Sent for review")),
        (WAITING_FOR_APPROVAL, _("Waiting for approval")),
        (APPROVED, _("Approved")),
    )

    CAN_EDIT = "metarecord.can_edit_classification"
    CAN_REVIEW = "metarecord.can_review_classification"
    CAN_APPROVE = "metarecord.can_approve_classification"
    CAN_VIEW_MODIFIED_BY = "metarecord.can_view_classification_modified_by"

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    version = models.PositiveIntegerField(
        db_index=True, default=1, null=True, blank=True
    )
    state = models.CharField(
        verbose_name=_("state"), max_length=20, choices=STATE_CHOICES, default=DRAFT
    )
    valid_from = models.DateField(verbose_name=_("valid from"), null=True, blank=True)
    valid_to = models.DateField(verbose_name=_("valid to"), null=True, blank=True)
    created_by = models.ForeignKey(
        get_user_model(),
        verbose_name=_("created by"),
        null=True,
        blank=True,
        related_name="%(class)s_created",
        editable=False,
        on_delete=models.SET_NULL,
    )
    modified_by = models.ForeignKey(
        get_user_model(),
        verbose_name=_("modified by"),
        null=True,
        blank=True,
        related_name="%(class)s_modified",
        editable=False,
        on_delete=models.SET_NULL,
    )
    _created_by = models.CharField(
        verbose_name=_("created by (text)"), max_length=200, blank=True, editable=False
    )
    _modified_by = models.CharField(
        verbose_name=_("modified by (text)"), max_length=200, blank=True, editable=False
    )

    parent = models.ForeignKey(
        "self",
        verbose_name=_("parent"),
        related_name="children",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    code = models.CharField(verbose_name=_("code"), max_length=16, db_index=True)
    title = models.CharField(verbose_name=_("title"), max_length=256)
    description = models.TextField(verbose_name=_("description"), blank=True)
    description_internal = models.TextField(
        verbose_name=_("description internal"), blank=True
    )
    related_classification = models.TextField(
        verbose_name=_("related classification"), blank=True
    )
    additional_information = models.TextField(
        verbose_name=_("additional information"), blank=True
    )
    function_allowed = models.BooleanField(
        verbose_name=_("function allowed"), default=False
    )

    objects = ClassificationQuerySet.as_manager()

    class Meta:
        verbose_name = _("classification")
        verbose_name_plural = _("classifications")
        unique_together = (("uuid", "version"),)
        permissions = (
            ("can_edit_classification", _("Can edit classification")),
            ("can_review_classification", _("Can review classification")),
            ("can_approve_classification", _("Can approve classification")),
            (
                "can_view_classification_modified_by",
                _("Can view classification modified by"),
            ),
        )

    def __str__(self):
        return self.code

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.id:
            with connection.cursor() as cursor:
                cursor.execute("LOCK TABLE %s" % self._meta.db_table)

            try:
                latest = Classification.objects.latest_version().get(code=self.code)
                self.version = latest.version + 1
                self.uuid = latest.uuid
            except Classification.DoesNotExist:
                self.version = 1

        # Only update `_created_by` and `_modified_by` value if the relations
        # are set set. Text values should persist even if related user is deleted.
        if self.created_by:
            self._created_by = self.created_by.get_full_name()

        if self.modified_by:
            self._modified_by = self.modified_by.get_full_name()

        super().save(*args, **kwargs)

        if self.state == Classification.APPROVED:
            # Delete old non-approved versions leading to current version if newly saved
            # version is approved.
            self.delete_old_non_approved_versions()

    def delete_old_non_approved_versions(self):
        if self.state != Classification.APPROVED:
            raise ValueError(
                "Function must be approved before old non-approved versions can be"
                " deleted."
            )

        Classification.objects.previous_versions(self).non_approved().delete()

    def get_modified_by_display(self):
        return self._modified_by or None


@transaction.atomic
def update_function_allowed(classifications):
    if not isinstance(classifications, Iterable):
        classifications = (classifications,)

    for classification in classifications:
        classification.function_allowed = not classification.children.exists()
        classification.save(update_fields=("function_allowed",))
