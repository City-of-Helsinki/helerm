import json

from django.contrib.postgres.forms import HStoreField


class UTF8HStoreField(HStoreField):
    """
    Disable non ASCII character escaping in HStoreField
    """
    def prepare_value(self, value):
        if isinstance(value, dict):
            return json.dumps(value, ensure_ascii=False)
        return value
