from django.conf import settings
from form_fields import parse_date_offset_string
import os
import subprocess
import csv
import ipdb

def pdf_to_images(pdf_file, image_path):
  media_root = settings.MEDIA_ROOT
  pdf = os.path.join(media_root, pdf_file)
  image = os.path.join(media_root, image_path)

  return subprocess.call(['convert', pdf, image])

def csv_to_offsets(csv_path):
  csv_file = open(os.path.join(settings.MEDIA_ROOT, csv_path), 'r')
  csv_reader = csv.reader(csv_file)

  offsets = []
  for row in csv_reader:
    offsets.append(parse_date_offset_string(row[0]))

  return offsets
