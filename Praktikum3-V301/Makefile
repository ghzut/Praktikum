all: build | build/*w.pdf python

python: 
	python *w.py
	
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

.PHONY: build all FORCE edittex python

