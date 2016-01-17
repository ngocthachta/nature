# this script joins all the pdfs inputs files to file results.pdf
gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=results.pdf $@
