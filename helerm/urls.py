from django.urls import include, path
from helusers import admin
from rest_framework.routers import DefaultRouter

from metarecord.views import AttributeViewSet, ClassificationViewSet, ExportView, FunctionViewSet, TemplateViewSet
from metarecord.views.export import JHSExportViewSet
from users.views import UserViewSet

router = DefaultRouter()
router.register(r'function', FunctionViewSet)
router.register(r'attribute', AttributeViewSet)
router.register(r'template', TemplateViewSet, base_name='template')
router.register(r'user', UserViewSet)
router.register(r'classification', ClassificationViewSet)
router.register(r'export/jhs191', JHSExportViewSet, base_name='jhs191_export')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('export/', ExportView.as_view(), name='export')
]
