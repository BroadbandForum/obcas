ARG FROM=broadbandforum/obcas-sdk:latest
FROM $FROM


ARG TAG=latest
ARG DOCKER-ORG=broadbandforum
ARG DOCKER-NAME=obcas-persister-app
ARG DOCKER-TAG=latest
ARG DOCKER-IMAGE=$(DOCKER-ORG)/$(DOCKER-NAME):$(DOCKER-TAG)
ARG DOCKER-CMD=bash

RUN pip3 install flask
RUN mkdir -p /obcas/netconf_requests/
RUN mkdir -p /obcas-pa
# copy source code
COPY ./opensearch_data/*.json /obcas-pa/
COPY ./nc_requests/*.xml /obcas/netconf_requests/
COPY ./bin/*.py /obcas-pa/
COPY ./opensearch_data/root-ca.pem /obcas-pa/root-ca.pem
RUN chmod -R 777 /obcas-pa/app.py
ENV PYTHONPATH=/obcas-pa
WORKDIR /obcas-pa

CMD python3 /obcas-pa/app.py