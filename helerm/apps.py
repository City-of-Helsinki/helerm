from django.apps import AppConfig


class HelermProjectConfig(AppConfig):
    name = "helerm"

    def ready(self):
        from auditlog_extra.utils import AuditLogConfigurationHelper

        AuditLogConfigurationHelper.raise_error_if_unconfigured_models()
