from django.conf import settings
from form_fields import parse_date_offset_string
import os
import subprocess
import csv
import ipdb
import logging

logger = logging.getLogger(__name__)

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

def presentation_to_pdf(presentation, pdf_file):
  logger.info("Converting presentation (%s) to pdf (%s)" % (presentation.event.name, pdf_file))
  images = [slide.image.path for slide in presentation.slide_set.slide_set.order_by("offset")]
  convert_call = ['convert']
  convert_call.extend(images)
  convert_call.extend([pdf_file])
  logger.info("Convert call: %s" % (' '.join(convert_call)))

  return subprocess.call(convert_call)

