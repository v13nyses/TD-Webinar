from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from presentations import forms
from presentations import utils

# Create your views here.
def UploadPdf(request):
  if request.method == "POST":
    form = forms.UploadPdfForm(request.POST, request.FILES)
    if form.is_valid():
      utils.extract_images(request.FILES['pdf_file'])
      return HttpResponseRedirect('/admin/')
  else:
    form = forms.UploadPdfForm()
  return render_to_response('upload.html', {'form': form})
