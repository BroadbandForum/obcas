# XXX seem to need to distclean before doing pip install .
distclean: clean
	$(RM) -rf build dist $(wildcard *.egg-info)

# docker targets
DOCKER-ORG = broadbandforum
DOCKER-NAME = obcas-persister-app
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

docker-push: docker-build
	docker image push $(DOCKER-IMAGE)
