FROM elasticsearch:7.3.2

# Installation of the voikko library and plugin for ElasticSearch
# https://github.com/EvidentSolutions/elasticsearch-analysis-voikko
RUN yum install -y \
    unzip \
    libvoikko

RUN curl -o /usr/lib64/voikko/morpho.zip https://www.puimula.org/htp/testing/voikko-snapshot/dict-morpho.zip
RUN unzip -o /usr/lib64/voikko/morpho.zip -d /usr/lib64/voikko/

RUN /usr/share/elasticsearch/bin/elasticsearch-plugin install --batch https://github.com/EvidentSolutions/elasticsearch-analysis-voikko/releases/download/v0.6.0/elasticsearch-analysis-voikko-0.6.0.zip \
&& echo '-Djava.security.policy=file:/usr/share/elasticsearch/plugins/elasticsearch-analysis-voikko/plugin-security.policy' >> /usr/share/elasticsearch/config/jvm.options \
|| echo "Plugin already exists."
