#current fluentd version used : 1.17.1
ARG FROM=fluent/fluentd:v1.17-1
FROM $FROM

USER root
RUN fluent-gem install fluent-plugin-opensearch -v 1.1.4
RUN fluent-gem install fluent-plugin-rewrite-tag-filter
#RUN mkdir -p /fluentd/tmp/
COPY fluent.conf /fluentd/etc/
USER fluent