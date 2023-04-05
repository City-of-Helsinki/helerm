from elasticsearch_dsl import analyzer, token_filter

from search_indices.utils import create_elasticsearch_connection


def get_finnish_stop_filter() -> token_filter:
    return token_filter("finnish_stop", type="stop", stopwords="_finnish_")


def get_finnish_stem_filter() -> token_filter:
    return token_filter("finnish_stemmer", type="stemmer", language="finnish")


def get_edge_ngram_filter() -> token_filter:
    return token_filter(
        "custom_edge_ngram_filter",
        type="edge_ngram",
        min_gram=3,
        max_gram=15,
    )


def get_raudikko_filter() -> token_filter:
    return token_filter(
        "raudikko",
        type="raudikko",
    )


def get_finnish_analyzer() -> analyzer:
    es_connection = create_elasticsearch_connection()
    if "raudikko" in es_connection.cat.plugins():
        return analyzer(
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
    else:
        return analyzer(
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
