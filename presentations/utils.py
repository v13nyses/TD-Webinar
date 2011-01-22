from pyPdf import PdfFileReader
from pyPdf.pdf import PageObject

def extract_images(pdf_file):
  #print pdf_file
  #print pdf_file.read()
  temp_file = open("temp_pdf", 'w')
  temp_file.write(pdf_file.read())
  temp_file.close()
  reader = PdfFileReader(open("temp_pdf"))
  i = 0
  doc_title = reader.documentInfo.title

  for p in reader.pages:
    print "page %d: %s" % (i, doc_title)
    i += 1
