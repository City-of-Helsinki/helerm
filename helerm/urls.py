from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from metarecord.views import (
    AttributeViewSet, BulkUpdateViewSet, ClassificationViewSet, ExportView, FunctionViewSet, JHSExportViewSet,
    RecordViewSet, TemplateViewSet
)
from users.views import UserViewSet

router = DefaultRouter()
router.register(r'function', FunctionViewSet)
router.register(r'record', RecordViewSet)
router.register(r'attribute', AttributeViewSet)
router.register(r'template', TemplateViewSet, basename='template')
router.register(r'user', UserViewSet)
router.register(r'classification', ClassificationViewSet)
router.register(r'export/jhs191', JHSExportViewSet, basename='jhs191_export')
router.register(r'bulk-update', BulkUpdateViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('export/', ExportView.as_view(), name='export')
]
