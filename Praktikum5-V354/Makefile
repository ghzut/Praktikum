all: python tex

python: *w.py matplotlibrc header-matplotlib.tex | build
	TEXINPUTS="$$(pwd):" python *w.py

tex: build/*w.pdf

build/*w.pdf: header.tex *w.tex lit.bib | build

build/*w.pdf: FORCE
	BIBINPUTS=build: \
	latexmk \
	 --lualatex \
	 --output-directory=build \
	 --interaction=nonstopmode \
	--halt-on-error \
	*w.tex

build:
	mkdir -p build

clean:
	rm -rf build

edittex:
	gnome-open *w.tex & ./makeloop.sh

FORCE:

.PHONY: build all FORCE edittex python tex
