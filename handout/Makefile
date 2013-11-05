all: pj3_description.pdf

pj3_description.pdf: pj3_description.ps
	ps2pdf pj3_description.ps

pj3_description.ps: pj3_description.dvi
	dvips -o pj3_description.ps pj3_description.dvi

pj3_description.dvi: pj3_description.tex
	latex pj3_description
	latex pj3_description
	latex pj3_description

clean:
	rm -f pj3_description.ps pj3_description.dvi pj3_description.aux pj3_description.log pj3_description.out pj3_description.pdf
