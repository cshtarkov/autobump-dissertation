DOT_FILES=$(wildcard images/dot/*.dot)
DOT_PDF_FILES=$(DOT_FILES:.dot=.pdf)

all: default

default: dissertation

images/dot/%.pdf: images/dot/%.dot
	dot -Tpdf -o $@ $<

images: $(DOT_PDF_FILES)

dissertation: images
	cp -v dissertation.tex dissertation.tex.bsed
	sed -i s'/\$$\$$/\$$/g' dissertation.tex
	pdflatex dissertation
	bibtex dissertation
	pdflatex dissertation
	pdflatex dissertation
	cp -fv dissertation.tex.bsed dissertation.tex
	rm -v dissertation.tex.bsed

clean:
	rm -f dissertation.tex.bsed
	rm -f dissertation.pdf
	rm -f *.aux *.bbl *.blg *.dvi
	rm -f images/dot/*.pdf
