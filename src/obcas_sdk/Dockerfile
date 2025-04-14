ARG FROM=broadbandforum/sphinx:latest
FROM $FROM

# install OS packages and create directories
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get --yes install \
        make \
        net-tools \
        iputils-ping \
        python3 \
        python3-pip \
        tshark \
        vim \
        kafkacat \
 && apt-get clean

RUN pip3 install confluent-kafka==2.4.0
ARG TAG=latest
ARG DOCKER-ORG=broadbandforum
ARG DOCKER-NAME=obcas-sdk
ARG DOCKER-TAG=latest
ARG DOCKER-IMAGE=$(DOCKER-ORG)/$(DOCKER-NAME):$(DOCKER-TAG)
ARG DOCKER-CMD=bash

RUN mkdir -p /obcas
RUN mkdir -p /obcas/dist/
# copy source code
COPY requirements.txt /obcas/requirements.txt

RUN PYTHONPATH=/obcas \
 && pip3 install -r /obcas/requirements.txt
COPY dist/obcas_sdk-1.0.0-py3-none-any.whl /obcas/dist/
ENV PYTHONPATH=/obcas
WORKDIR /obcas
RUN pip3 install  /obcas/dist/obcas_sdk-1.0.0-py3-none-any.whl

CMD ["python3 -V"]