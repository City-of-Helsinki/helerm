from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from helusers import admin

from metarecord.views import AttributeViewSet, ClassificationViewSet, FunctionViewSet, ExportView, TemplateViewSet
from users.views import UserViewSet


router = DefaultRouter()
router.register(r'function', FunctionViewSet)
router.register(r'attribute', AttributeViewSet)
router.register(r'template', TemplateViewSet, base_name='template')
router.register(r'user', UserViewSet)
router.register(r'classification', ClassificationViewSet)

urlpatterns = [
    url(r'^v1/', include(router.urls, namespace='v1')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^export/', ExportView.as_view(), name='export')
]
