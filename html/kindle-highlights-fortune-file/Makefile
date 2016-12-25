.PHONY: clean
clean:
	rm -f fortunes fortunes.dat

fortunes:
	python kindle-to-fortune.py

.PHONY: build
build: clean fortunes

.PHONY: fortune
fortune: fortunes
	@echo
	@fortune ./fortunes
	@echo
