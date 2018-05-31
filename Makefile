# A simple makefile for creating the Turbine Client distribution file
##########################################################################
# Joshua R. Boverhof, LBNL
# See LICENSE.md for copyright notice!
###########################################################################
VERSION := $(shell git describe --tags --dirty)
PRODUCT=Turbine Client Scripts
PROD_SNAME=turb_client
LICENSE=LICENSE.md
TARGET_NAME=CCSI_$(PROD_SNAME)_$(VERSION)


# OS detection & changes
UNAME := $(shell uname)
ifeq ($(UNAME), Linux)
  MD5BIN=md5sum
endif
ifeq ($(UNAME), Darwin)
  MD5BIN=md5
endif
ifeq ($(UNAME), FreeBSD)
  MD5BIN=md5
endif

.DEFAULT_GOAL := all

### 
### DIRECT TARGETS
### 
$(TARGET_NAME).tar.gz: $(LICENSE) 
	@python setup.py -q sdist --formats=gztar
	@cp dist/TurbineClient-$(VERSION).tar.gz $@
	@$(MD5BIN) $@

$(TARGET_NAME).zip: $(LICENSE) 
	@python setup.py -q sdist --formats=zip
	@cp dist/TurbineClient-$(VERSION).zip $@
	@$(MD5BIN) $@

### 
### PHONY TARGETS
### 
.PHONY: all
all: zip tar

.PHONY: tar
tar: $(TARGET_NAME).tar.gz

.PHONY: zip
zip: $(TARGET_NAME).zip

.PHONY: clean
clean:
	@\rm -rf dist TurbineClient.egg-info

.PHONY: distclean
distclean: clean
	@rm -f $(TARGET_NAME).zip
	@rm -f $(TARGET_NAME).tar.gz
