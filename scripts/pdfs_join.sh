# this script joins all the pdfs inputs files to file results.pdf
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dDownsampleColorImages=true \
-dColorImageResolution=100 -dPDFSETTING=/ebook -dNOPAUSE -dQUIET -dBATCH \
-sOutputFile=results.pdf $@
