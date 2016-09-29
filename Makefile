all: default
default: dissertation
dissertation:
	pdflatex dissertation
	bibtex dissertation
	pdflatex dissertation
	pdflatex dissertation
clean:
	rm -f dissertation.pdf
	rm -f *.aux *.bbl *.blg *.dvi
