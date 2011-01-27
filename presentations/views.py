from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from presentations import forms
from presentations import utils
from presentations.models import Slide, Presentation
from polls.models import Poll
from polls.views import vote
import simplejson as json


# Create your views here.
def UploadPdf(request):
  if request.method == "POST":
    form = forms.UploadPdfForm(request.POST, request.FILES)
    if form.is_valid():
      image_files = utils.extract_images(request.FILES['pdf_file'])
      
      for img in image_files:
        pass
        #slide = Slide({'image': )        

      #utils.remove_images(image_files)

      return HttpResponseRedirect('/admin/')
  else:
    form = forms.UploadPdfForm()
  return render_to_response('upload.html', {'form': form})

def displaySlide(request, slide_id = None):
  try:
    poll = Poll.objects.get(id=slide_id)
    return vote(request, slide_id)
  except ObjectDoesNotExist, e:
    slide = get_object_or_404(Slide, pk=slide_id)
    return render_to_response('presentations/slide.html', {'slide': slide},
                              context_instance = RequestContext(request))

def queuePoints(request, presentation_id = None):
  try:
    presentation = Presentation.objects.get(id = presentation_id)
    print presentation
    queue_points = presentation.queuepoint_set.order_by('-time_offset')
    
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
