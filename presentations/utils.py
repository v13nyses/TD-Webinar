from pyPdf import PdfFileReader
from pyPdf.pdf import PageObject

def extract_images(pdf_file):
  reader = PdfFileReader(pdf_file)
  i = 0

  for p in reader.pages:
    print "page %d: %s" % (i, p.documentInfo.title)
    i += 1
