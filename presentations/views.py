from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from presentations import forms
from presentations import utils
from presentations.models import Slide

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

def displaySlide(request, slide_id = None):
  slide = Slide.objects.get(id=slide_id)

  if isinstance(slide, Slide):
    print "is slide"
  else:
    print "is not slide"
  print slide

  return render_to_response('slide.html', {'slide': slide},
                            context_instance = RequestContext(request))
      
