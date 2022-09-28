SOURCES=$(wildcard html/*/*.html)
RAW_DATA=$(SOURCES:html/%.html=raw_data/%.csv)
TARGETS=$(RAW_DATA)

.DELETE_ON_ERROR:
.PHONY: default

default: $(TARGETS)

debug:
	@echo $(RAW_DATA)

raw_data/%.csv: html/%.html
	@mkdir -p `dirname $@`
	python bwssb.py parse $< > $@

load:
	python bwssb.py load-db raw_data/*/*.csv

clean:
	-rm $(TARGETS)