from .settings import *  # noqa


# Prefix all indices with test_ to avoid conflicts with production indices
ELASTICSEARCH_INDEX_NAMES = {
    k: f"test_{v}"
    for k, v in ELASTICSEARCH_INDEX_NAMES.items()  # noqa: F405
}
