from django.http import HttpResponse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from presentations import forms
from presentations import utils
from presentations.models import Slide, Presentation
import simplejson as json

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

def queuePoints(request, presentation_id = None):
  try:
    presentation = Presentation.objects.get(id = presentation_id)
    print presentation
    queue_points = presentation.queuepoint_set.all()
    
  except:
    print 'except'
    presentation = None
    queue_points = []

  queue_points_raw = []
  for queue_point in queue_points:
    queue_points_raw.append({
      'slideId': queue_point.slide.id,
      'timeOffset': queue_point.time_offset
    })

  return HttpResponse(json.dumps(queue_points_raw), mimetype = 'application/javascript')
