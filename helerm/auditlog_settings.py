# Register all models by default (False by default)
AUDITLOG_INCLUDE_ALL_MODELS = True

# Exclude the IP address from logging. (False by default)
# When using “AuditlogMiddleware”, the IP address is logged by default
AUDITLOG_DISABLE_REMOTE_ADDR = False

# Disables logging during raw save. (I.e. for instance using loaddata)
# M2M operations will still be logged, since they’re never considered raw.
# (False by default)
AUDITLOG_DISABLE_ON_RAW_SAVE = True

# Exclude models in registration process.
# This setting will only be considered when AUDITLOG_INCLUDE_ALL_MODELS is True.
AUDITLOG_EXCLUDE_TRACKING_MODELS = (
    "admin.logentry",  # excluded by default
    "auditlog.logentry",  # excluded by default
    "contenttypes.contenttype",  # system model
    "sessions.session",  # auth model
    "helusers.oidcbackchannellogoutevent",  # auth model
    # social-auth-app-django models
    # https://github.com/python-social-auth/social-app-django/blob/master/social_django/models.py
    "social_django.association",  # auth model
    "social_django.code",  # auth model
    "social_django.nonce",  # auth model
    "social_django.partial",  # auth model
    "social_django.usersocialauth",  # auth model
    "resilient_logger.resilientlogentry",  # resilient log entries
)

# Configure models registration and other behavior.
AUDITLOG_INCLUDE_TRACKING_MODELS = (
    "users.user_user_permissions",
    "users.user_groups",
    "users.user_ad_groups",
    "auth.group_permissions",
    "helusers.adgroup",
    "helusers.adgroupmapping",
    "auth.permission",
    {
        "model": "auth.group",
        "m2m_fields": ["permissions"],
    },
    {
        "model": "users.user",
        "m2m_fields": ["groups", "user_permissions", "ad_groups"],
        "exclude_fields": [
            "last_login",  # don't write log of every request
            "last_api_use",  # helusers internal, changes daily
        ],
        "mask_fields": [
            "first_name",
            "last_name",
            "email",
            "password",
        ],
        "serialize_data": True,
        "serialize_auditlog_fields_only": True,
    },
    "sites.site",
    "metarecord.phase",
    "metarecord.metadataversion",
    "metarecord.attributevalue",
    "metarecord.record",
    "metarecord.function",
    "metarecord.action",
    "metarecord.attribute",
    "metarecord.classification",
    "metarecord.attributegroup",
    "metarecord.attributevalidationrule",
    "metarecord.bulkupdate",
)

AUDITLOG_MASK_CALLABLE = "helerm.auditlog_settings.custom_mask"


def custom_mask(value):
    return "*"
