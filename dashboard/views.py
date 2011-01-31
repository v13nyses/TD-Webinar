from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
import form_utils
from forms import EventForm
from events.models import Event, event_upload_to
from presentations.models import Video

def upload_file(event, uploaded_file):
  print event_upload_to(event, uploaded_file.name)

# used by urls:
#   dashboard/event/add/
#   dashboard/event/<event_id>/
#   dashboard/
def event(request, event_id = None):
  if request.POST:
    event_form = EventForm(request.POST, request.FILES)
    if event_form.is_valid():
      event_form.save()

  else:
    event_form = EventForm()

  return render_to_response('dashboard/event.html', {'event_form': event_form}, 
                            context_instance = RequestContext(request))
 
# used by urls:
#   dashboard/slides/add/ 
def slides(request):
  # TO DO
  pass
  
# used by urls:
#   dashboard/slide/<slide_id>/ 
def slide(request, slide_id = None):
  # TO DO
  pass
  
# used by urls:
#   dashboard/presenters/add/ 
def presenters(request):
  # TO DO
  pass
  
# used by urls:
#   dashboard/presenter/<presenter_id>/
def presenter(request, presenter_id = None):
  # TO DO
  pass
  
# used by urls:
#   dashboard/preview/
#   dashboard/preview/pre
def pre(request):
  # TO DO
  pass
  
# used by urls:
#   dashboard/preview/lobby/
def lobby(request):
  # TO DO
  pass
  
# used by urls:
#   dashboard/preview/live/
def live(request):
  # TO DO
  pass
  
# used by urls:
#   dashboard/preview/post/
def post(request):
  # TO DO
  pass
  
# used by urls:
#   dashboard/preview/archive/
def archive(request):
  # TO DO
  pass
  
# used by urls:
#   dashboard/preview/email/ 
def email(request):
  # TO DO
  pass
  
