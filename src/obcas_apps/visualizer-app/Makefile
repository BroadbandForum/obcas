DOCKER-ORG = broadbandforum
DOCKER-NAME = alarm-correlation-visualizer-webapp
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
	npm install && docker image build $(DOCKER-BUILDOPTS) --tag=$(DOCKER-ORG)/$(DOCKER-NAME) .

docker-push: docker-build
	docker image push $(DOCKER-IMAGE)

clean:
	rm -r node_modules && rm package-lock.json

