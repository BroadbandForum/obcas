# docker targets
DOCKER-ORG = broadbandforum
DOCKER-NAME = obcas-fluentd
DOCKER-TAG = v1.17-1
DOCKER-IMAGE = $(DOCKER-ORG)/$(DOCKER-NAME):$(DOCKER-TAG)
DOCKER-CMD = bash

DOCKER-BUILDOPTS =
ifneq "$(FROM)" ""
  DOCKER-BUILDOPTS += --build-arg FROM=$(FROM)
endif
ifneq "$(NOCACHE)" ""
  DOCKER-BUILDOPTS += --no-cache
endif


docker-build:
	docker image build $(DOCKER-BUILDOPTS) --tag=$(DOCKER-ORG)/$(DOCKER-NAME):$(DOCKER-TAG) .

docker-push: docker-build
	docker image push $(DOCKER-IMAGE)
