import os
import subprocess
from time import time

from pyPdf import PdfFileReader
from pyPdf.pdf import PageObject

from settings import TEMP_URL

def extract_images(pdf_file):
  #print pdf_file
  #print pdf_file.read()
  temp_file_path = os.path.join(TEMP_URL, "%d_temp.pdf" % (int(time())))
  temp_file = open(temp_file_path, 'w')
  temp_file.write(pdf_file.read())
  temp_file.close()
  reader = PdfFileReader(open(temp_file_path))
  cmd = ["convert", temp_file_path, "%s.png" % temp_file_path]
  print cmd
  p = subprocess.Popen(cmd)

  #rc = p.wait()

  #if rc:
  #  print "something went wrong.."
