# A simple makefile for creating the Turbine Client distribution file
##########################################################################
# Joshua R. Boverhof, LBNL
# See Copyright for copyright notice!
###########################################################################
VERSION := $(shell python -c "import turbine; print '%s' % turbine.__version__")
PRODUCT=Turbine Client Scripts
PROD_SNAME=turb_client
LICENSE=CCSI_TE_LICENSE_$(PROD_SNAME).txt
TARGET_NAME=CCSI_$(PROD_SNAME)_$(VERSION)

# Where Jenkins should checkout ^/projects/common/trunk/
COMMON=.ccsi_common

LEGAL_DOCS=LLNL_Notice3.txt \
           LEGAL \
           CCSI_TE_LICENSE.txt

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
$(TARGET_NAME).tar.gz: $(LICENSE) $(LEGAL_DOCS)
	@python setup.py -q sdist --formats=gztar
	@cp dist/TurbineClient-$(VERSION).tar.gz $@
	@$(MD5BIN) $@

$(TARGET_NAME).zip: $(LICENSE) $(LEGAL_DOCS)
	@python setup.py -q sdist --formats=zip
	@cp dist/TurbineClient-$(VERSION).zip $@
	@$(MD5BIN) $@

$(LICENSE): CCSI_TE_LICENSE.txt
	@sed "s/\[SOFTWARE NAME \& VERSION\]/$(PRODUCT) v.$(VERSION)/" < CCSI_TE_LICENSE.txt > $(LICENSE)

$(LEGAL_DOCS):
	@if [ -d $(COMMON) ]; then \
	  cp $(COMMON)/$@ .; \
	else \
	  svn -q export ^/projects/common/trunk/$@; \
	fi

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
	@\rm -rf $(LICENSE) $(LEGAL_DOCS) dist TurbineClient.egg-info

.PHONY: distclean
distclean: clean
	@rm -f $(TARGET_NAME).zip
	@rm -f $(TARGET_NAME).tar.gz
