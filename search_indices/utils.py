from django.conf import settings
from elasticsearch_dsl import analyzer, connections, token_filter


def create_elasticsearch_connection():
    return connections.create_connection(**settings.ELASTICSEARCH_DSL["default"])


def get_finnish_stop_filter() -> token_filter:
    return token_filter("finnish_stop", type="stop", stopwords="_finnish_")


def get_finnish_stem_filter() -> token_filter:
    return token_filter("finnish_stemmer", type="stemmer", language="finnish")


def get_edge_ngram_filter() -> token_filter:
    return token_filter(
        "custom_edge_ngram_filter", type="edge_ngram", min_gram=3, max_gram=15
    )


def get_raudikko_filter() -> token_filter:
    return token_filter("raudikko", type="raudikko")


finnish_raudikko_analyzer = analyzer(
    "finnish_analyzer",
    tokenizer="finnish",
    filter=[
        "lowercase",
        "asciifolding",
        "unique",
        get_edge_ngram_filter(),
        get_raudikko_filter(),
    ],
)

finnish_standard_analyzer = analyzer(
    "finnish_analyzer",
    tokenizer="standard",
    filter=[
        "lowercase",
        "asciifolding",
        "unique",
        get_edge_ngram_filter(),
        get_finnish_stop_filter(),
        get_finnish_stem_filter(),
    ],
)


def get_finnish_analyzer(mode: str) -> analyzer:
    if mode == "probe":
        es_connection = create_elasticsearch_connection()
        es_plugins = es_connection.cat.plugins()
        mode = "raudikko" if "raudikko" in es_plugins else "standard"

    if mode == "raudikko":
        return finnish_raudikko_analyzer
    elif mode == "standard":
        return finnish_standard_analyzer

    raise ValueError(
        "Invalid argument. Possible values are: probe, raudikko and standard."
    )
