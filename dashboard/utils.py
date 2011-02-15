from django.conf import settings
import os
import subprocess
import ipdb

def pdf_to_images(pdf_file, image_path):
  media_root = settings.MEDIA_ROOT
  pdf = os.path.join(media_root, pdf_file)
  image = os.path.join(media_root, image_path)

  return subprocess.call(['convert', pdf, image])
