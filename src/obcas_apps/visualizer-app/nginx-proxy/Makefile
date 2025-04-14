DOCKER-ORG = broadbandforum
DOCKER-NAME = alarm-correlation-visualizer-nginx-webapp
DOCKER-TAG = latest
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
	docker image build $(DOCKER-BUILDOPTS) --tag=$(DOCKER-ORG)/$(DOCKER-NAME) .

docker-push:
	docker image push $(DOCKER-IMAGE)
