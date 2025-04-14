FROM nginx:1.27.1

COPY ./conf /etc/nginx

ENV DOLLAR="$" \
    OPENSEARCH_SERVER="localhost" \
    ALARM_CORRELATION_SERVER="localhost" \
    SERVER_NAME="localhost" \
    SERVER_PORT="443"

ENTRYPOINT ["/bin/bash", "-c", "envsubst < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && exec /docker-entrypoint.sh nginx -g 'daemon off;'"]

