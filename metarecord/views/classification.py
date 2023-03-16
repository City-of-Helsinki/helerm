import django_filters
from django.core import exceptions
from django.db import transaction
from django.db.models import Prefetch, Q
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, viewsets

from metarecord.models import Classification, Function
from metarecord.views.base import ClassificationRelationSerializer
from metarecord.views.function import PhaseSerializer


def include_related(request):
    """
    Convert 'include_related' GET parameter value to boolean.
    Accept 'true' and 'True' as valid values.
    """
    query_param_value = request.GET.get("include_related")
    return query_param_value in ["true", "True"]


class ClassificationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="uuid", format="hex", read_only=True)
    parent = ClassificationRelationSerializer(required=False)
    modified_by = serializers.SerializerMethodField()
    version_history = serializers.SerializerMethodField()

    class Meta:
        model = Classification
        fields = (
            "id",
            "created_at",
            "modified_at",
            "modified_by",
            "version",
            "state",
            "valid_from",
            "valid_to",
            "code",
            "title",
            "parent",
            "description",
            "description_internal",
            "related_classification",
            "additional_information",
            "function_allowed",
            "version_history",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context["request"]
        self.include_related = False

        if request.method == "GET":
            self.include_related = include_related(request)

    def get_fields(self):
        user = self.context["request"].user
        fields = super().get_fields()

        if self.include_related:
            fields["phases"] = serializers.SerializerMethodField(
                method_name="_get_phases"
            )

        if not user.has_perm(Classification.CAN_VIEW_MODIFIED_BY):
            del fields["modified_by"]

        return fields

    def get_modified_by(self, obj):
        return obj.get_modified_by_display()

    def _get_function(self, obj):
        functions = obj.prefetched_functions
        num_of_functions = len(functions)

        if num_of_functions > 1:
            raise ValueError(
                "Classification %s has more than one functions (%s)"
                % (obj.uuid, [function.uuid for function in functions])
            )

        return functions[0] if num_of_functions else None

    def _append_function_fields_to_repr(self, obj, data):
        function = self._get_function(obj)
        if function:
            data["function"] = function.uuid.hex
            data["function_state"] = function.state
            data["function_attributes"] = function.attributes
            data["function_version"] = function.version
            data["function_valid_from"] = function.valid_from
            data["function_valid_to"] = function.valid_to
        else:
            data["function"] = None
            data["function_state"] = None
            data["function_attributes"] = None
            data["function_version"] = None
            data["function_valid_from"] = None
            data["function_valid_to"] = None

        return data

    def _get_phases(self, obj):
        phases = None
        function = self._get_function(obj)

        if function:
            phases = function.phases.all()

        serializer = PhaseSerializer(phases, many=True)

        return serializer.data

    def get_version_history(self, obj):
        request = self.context["request"]
        classifications = (
            Classification.objects.filter_for_user(request.user)
            .filter(uuid=obj.uuid)
            .order_by("version")
        )
        ret = []

        for classification in classifications:
            version_data = {
                attr: getattr(classification, attr)
                for attr in (
                    "state",
                    "version",
                    "modified_at",
                    "valid_from",
                    "valid_to",
                )
            }

            if not request or request.user.has_perm(
                Classification.CAN_VIEW_MODIFIED_BY
            ):
                version_data["modified_by"] = classification.get_modified_by_display()

            ret.append(version_data)

        return ret

    def to_representation(self, obj):
        data = super().to_representation(obj)
        request = self.context["request"]

        if request and request.method == "GET":
            data = self._append_function_fields_to_repr(obj, data)

            if not request.user.is_authenticated:
                data.pop("description_internal", None)
                data.pop("additional_information", None)

        return data

    def _create_new_version(self, validated_data):
        user = self.context["request"].user
        user_data = {"created_by": user, "modified_by": user}
        validated_data.update(user_data)
        return Classification.objects.create(**validated_data)

    def validate(self, data):
        request = self.context["request"]
        if request.method in ["PUT", "PATCH"]:
            self.validate_update(data)
        return super().validate(data)

    def validate_update(self, data):
        if self.partial:
            if not any(field in data for field in ("state", "valid_from", "valid_to")):
                raise exceptions.ValidationError(
                    _('"state", "valid_from" or "valid_to" required.')
                )

            new_state = data.get("state")
            if new_state:
                self.validate_state_change(self.instance.state, new_state)

    def validate_state_change(self, old_state, new_state):
        user = self.context["request"].user

        if old_state == new_state:
            return

        valid_changes = {
            Classification.DRAFT: {Classification.SENT_FOR_REVIEW},
            Classification.SENT_FOR_REVIEW: {
                Classification.WAITING_FOR_APPROVAL,
                Classification.DRAFT,
            },
            Classification.WAITING_FOR_APPROVAL: {
                Classification.APPROVED,
                Classification.DRAFT,
            },
            Classification.APPROVED: {Classification.DRAFT},
        }

        if new_state not in valid_changes[old_state]:
            raise exceptions.ValidationError({"state": [_("Invalid state change.")]})

        state_change_required_permissions = {
            Classification.SENT_FOR_REVIEW: Classification.CAN_EDIT,
            Classification.WAITING_FOR_APPROVAL: Classification.CAN_REVIEW,
            Classification.APPROVED: Classification.CAN_APPROVE,
        }

        relevant_state = new_state if new_state != Classification.DRAFT else old_state
        required_permission = state_change_required_permissions[relevant_state]

        if not user.has_perm(required_permission):
            raise exceptions.PermissionDenied(_("No permission for the state change."))

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user

        if not user.has_perm(Classification.CAN_EDIT):
            raise exceptions.PermissionDenied(_("No permission to create."))

        validated_data.update(
            {
                "created_by": user,
                "modified_by": user,
            }
        )

        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        user = self.context["request"].user

        if not user.has_perm(Classification.CAN_EDIT):
            raise exceptions.PermissionDenied(_("No permission to update."))

        if self.partial:
            allowed_fields = {"state", "valid_from", "valid_to"}
            data = {
                field: validated_data[field]
                for field in allowed_fields
                if field in validated_data
            }
            if not data:
                return instance
            data["modified_by"] = user

            # Update only state, valid_from and valid_to fields
            # and do an actual update instead of a new version
            return super().update(instance, data)

        if instance.state in (
            Classification.SENT_FOR_REVIEW,
            Classification.WAITING_FOR_APPROVAL,
        ):
            raise exceptions.ValidationError(
                _(
                    'Cannot edit while in state "sent_for_review" or "waiting_for_approval"'
                )
            )

        return self._create_new_version(validated_data)


class ClassificationFilterSet(django_filters.FilterSet):
    valid_at = django_filters.DateFilter(method="filter_valid_at")

    class Meta:
        model = Classification
        fields = ("valid_at", "version")

    def filter_valid_at(self, queryset, name, value):
        # Classification is considered invalid if neither date is set
        queryset = queryset.exclude(valid_from__isnull=True, valid_to__isnull=True)

        # Null value means there's no bound to that direction
        queryset = queryset.filter(
            (Q(valid_from__isnull=True) | Q(valid_from__lte=value))
            & (Q(valid_to__isnull=True) | Q(valid_to__gte=value))
        )
        return queryset


class ClassificationViewSet(viewsets.ModelViewSet):
    queryset = (
        Classification.objects.order_by("code")
        .select_related("parent")
        .prefetch_related("children")
    )
    serializer_class = ClassificationSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = ClassificationFilterSet
    lookup_field = "uuid"

    def apply_queryset_filters(self, queryset):
        queryset = queryset.filter_for_user(self.request.user)

        if "version" in self.request.query_params:
            return queryset

        state = self.request.query_params.get("state")
        if state == "approved":
            return queryset.latest_approved()

        return queryset.latest_version()

    def get_queryset(self):
        user = self.request.user
        function_qs = Function.objects.filter_for_user(user).latest_version()

        if include_related(self.request):
            function_qs = function_qs.prefetch_related(
                "phases", "phases__actions", "phases__actions__records"
            )

        queryset = super().get_queryset()
        queryset = self.apply_queryset_filters(queryset)

        return queryset.prefetch_related(
            Prefetch("functions", queryset=function_qs, to_attr="prefetched_functions")
        )
