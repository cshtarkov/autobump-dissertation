DOT_FILES=$(wildcard images/dot/*.dot)
DOT_PDF_FILES=$(DOT_FILES:.dot=.pdf)

all: default

default: dissertation

images/dot/%.pdf: images/dot/%.dot
	dot -Tpdf -o $@ $<

images: $(DOT_PDF_FILES)

dissertation: images
	pdflatex dissertation
	bibtex dissertation
	pdflatex dissertation
	pdflatex dissertation

clean:
	rm -f dissertation.pdf
	rm -f *.aux *.bbl *.blg *.dvi
	rm -f images/dot/*.pdf
