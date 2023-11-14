from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_safe
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter

from metarecord.views import (
    AttributeViewSet,
    BulkUpdateViewSet,
    ClassificationViewSet,
    ExportView,
    FunctionViewSet,
    JHSExportViewSet,
    RecordViewSet,
    TemplateViewSet,
)
from search_indices.views import (
    ActionSearchDocumentViewSet,
    AllSearchDocumentViewSet,
    ClassificationSearchDocumentViewSet,
    FunctionSearchDocumentViewSet,
    PhaseSearchDocumentViewSet,
    RecordSearchDocumentViewSet,
)
from users.views import UserViewSet

router = DefaultRouter()
router.register(r"function", FunctionViewSet)
router.register(r"record", RecordViewSet)
router.register(r"attribute", AttributeViewSet)
router.register(r"template", TemplateViewSet, basename="template")
router.register(r"user", UserViewSet)
router.register(r"classification", ClassificationViewSet)
router.register(r"export/jhs191", JHSExportViewSet, basename="jhs191_export")
router.register(r"bulk-update", BulkUpdateViewSet)
router.register(r"action-search", ActionSearchDocumentViewSet, basename="action_search")
router.register(
    r"classification-search",
    ClassificationSearchDocumentViewSet,
    basename="classification_search",
)
router.register(
    r"function-search", FunctionSearchDocumentViewSet, basename="function_search"
)
router.register(r"phase-search", PhaseSearchDocumentViewSet, basename="phase_search")
router.register(r"record-search", RecordSearchDocumentViewSet, basename="record_search")
router.register(r"all-search", AllSearchDocumentViewSet, basename="all_search")


#
# Kubernetes liveness & readiness probes
#
@require_safe
@never_cache
def healthz(*_, **__):
    return HttpResponse(status=200)


@require_safe
@never_cache
def readiness(*_, **__):
    return HttpResponse(status=200)


urlpatterns = [
    path("healthz", healthz),
    path("readiness", readiness),
    path("v1/", include(router.urls)),
    path("admin/", admin.site.urls),
    path("pysocial/", include("social_django.urls", namespace="social")),
    path("helauth/", include("helusers.urls")),
    path("export/", ExportView.as_view(), name="export"),
    path("", RedirectView.as_view(url="v1/")),
]
