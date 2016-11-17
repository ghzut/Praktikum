all: build tex python

python:
	python *w.py

tex: build/*w.pdf

build/*w.pdf: header.tex *w.tex lit.bib

build/*w.pdf: FORCE
	latexmk --lualatex --output-directory=build --interaction=nonstopmode *w.tex

build:
	mkdir -p build

clean:
	rm -rf build

edittex:
	gnome-open *w.tex & ./makeloop.sh

FORCE:

.PHONY: build all FORCE edittex python tex
