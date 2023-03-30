from django.conf import settings

from search_indices.utils import get_finnish_analyzer

FINNISH_ANALYZER = get_finnish_analyzer(settings.ELASTICSEARCH_ANALYZER_MODE)
