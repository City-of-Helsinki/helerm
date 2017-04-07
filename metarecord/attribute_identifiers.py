ADDITIONAL_INFORMATION = 'AdditionalInformation'
INFORMATION_SYSTEM = 'InformationSystem'
PERSONAL_DATA = 'PersonalData'
PROTECTION_CLASS = 'ProtectionClass'
PUBLICITY_CLASS = 'PublicityClass'
RESTRICTION__PROTECTION_LEVEL = 'Restriction.ProtectionLevel'
RESTRICTION__SECURITY_CLASS = 'Restriction.SecurityClass'
RESTRICTION__SECURITY_PERIOD_START = 'Restriction.SecurityPeriodStart'
RETENTION_PERIOD = 'RetentionPeriod'
RETENTION_PERIOD_OFFICE = 'RetentionPeriodOffice'
RETENTION_PERIOD_START = 'RetentionPeriodStart'
RETENTION_PERIOD_TOTAL = 'RetentionPeriodTotal'
RETENTION_REASON = 'RetentionReason'
SECURITY_PERIOD = 'SecurityPeriod'
SECURITY_REASON = 'SecurityReason'
SOCIAL_SECURITY_NUMBER = 'SocialSecurityNumber'
STORAGE_ACCOUNTABLE = 'StorageAccountable'
STORAGE_LOCATION = 'StorageLocation'
STORAGE_ORDER = 'StorageOrder'
SUBJECT = 'Subject'
SUBJECT__SCHEME = 'Subject.Scheme'




def create_constants():
    attrs = []
    for attr in ATTRIBUTES:
        identifier = attr['identifier']
        constant = identifier
        constant.replace('.', ' ')
        attrs.append("%s = '%s'" % (constant.upper(), attr['identifier']))

    for attr in sorted(attrs):
        print(attr)
