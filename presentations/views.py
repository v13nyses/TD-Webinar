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
      utils.extract_images(request.FILES['pdf_file'])
      return HttpResponseRedirect('/admin/')
  else:
    form = forms.UploadPdfForm()
  return render_to_response('upload.html', {'form': form})

def displaySlide(request, slide_id = None):
  slide = get_object_or_404(Slide, pk=slide_id)
  slide = slide.as_leaf_class()
  return slide.display(request, slide)

#  try:
#    poll = Poll.objects.get(id=slide_id)
#    return vote(request, slide_id)
#  except ObjectDoesNotExist, e:
#    slide = get_object_or_404(Slide, pk=slide_id)
#    return render_to_response('presentations/slide.html', {'slide': slide},
#                              context_instance = RequestContext(request))

def displaySlideSet(request, presentation_id = None):
  try:
    presentation = Presentation.objects.get(id = presentation_id)
    slides = Slide.objects.filter(slide_set = presentation.slide_set).order_by('-offset')
    
  except:
    presentation = None
    slides = []

  slides_data = []
  for slide in slides:
    slides_data.append({
      'slideId': slide.id,
      'timeOffset': slide.offset
    })

  return HttpResponse(json.dumps(slides_data), mimetype = 'application/javascript')

def video_player(request, video_id, player_id):
  url = settings.VIDEO_URL % (video_id, player_id)
  return render_to_response('presentations/video_player.html', {'url': url})
