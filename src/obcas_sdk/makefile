# default target
html:

# docker targets
DOCKER-ORG = broadbandforum
DOCKER-NAME = obcas-sdk
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

# distribution targets
dist:
	python3 setup.py bdist_wheel
	sudo pip3 install ./dist/obcas_sdk-1.0.0-py3-none-any.whl
	docker image build $(DOCKER-BUILDOPTS) --tag=$(DOCKER-ORG)/$(DOCKER-NAME) .

# XXX seem to need to distclean before doing pip install .
distclean:
	sudo pip3 uninstall ./dist/obcas_sdk-1.0.0-py3-none-any.whl --yes
	$(RM) -rf build dist $(wildcard *.egg-info)
