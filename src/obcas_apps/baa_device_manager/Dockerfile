ARG FROM=broadbandforum/obcas-sdk:latest
FROM $FROM


ARG TAG=latest
ARG DOCKER-ORG=broadbandforum
ARG DOCKER-NAME=baa-device-manager
ARG DOCKER-TAG=latest
ARG DOCKER-IMAGE=$(DOCKER-ORG)/$(DOCKER-NAME):$(DOCKER-TAG)
ARG DOCKER-CMD=bash

RUN mkdir -p /obcas/netconf_requests/
COPY ./nc_requests/*.xml /obcas/netconf_requests/
RUN mkdir -p /obcas-dm
# copy source code
COPY . /obcas-dm
ENV PYTHONPATH=/obcas-dm
WORKDIR /obcas-dm
RUN pip3 install --upgrade streamlit
RUN pip3 install streamlit_option_menu
RUN pip3 install streamlit-extras

EXPOSE 8051

CMD ["python3 -V"]
CMD streamlit run /obcas-dm/app.py