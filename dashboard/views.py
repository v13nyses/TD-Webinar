from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from form_controllers import EventFormController, PresentationFormController
from events.models import Event
from presentations.models import Presenter

# used by urls:
#   dashboard/event/add/
#   dashboard/event/<event_id>/
#   dashboard/
def event(request, event_id = None):
  if event_id != None:
    event = Event.objects.get(id = event_id)
    controller = EventFormController(request, event)
  else: 
    controller = EventFormController(request)

  if controller.save():
    id = controller.form.instance.id
    return HttpResponseRedirect('/dashboard/event/%d/presenters/add' % id)

  return render_to_response('dashboard/event.html', {'form': controller.form, 'form_url': request.META['PATH_INFO']}, 
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
#   dashboard/<event_id>/presenters/add/ 
def presenters(request, event_id = None):
  event = Event.objects.get(id = event_id)
  controller = PresentationFormController(request)
  controller.save(event)

  return render_to_response('dashboard/presentation.html', {'form': controller.form, 'form_url': request.META['PATH_INFO'], 'event': event}, 
                            context_instance = RequestContext(request))
  
# used by urls:
#   dashboard/<event_id>/presenter/<presenter_id>/
def presenter(request, event_id = None, presenter_id = None, action = 'save'):
  event = Event.objects.get(id = event_id)
  presenter = Presenter.objects.get(id = presenter_id)
  controller = PresentationFormController(request, instance = presenter)

  if action == 'save':
    controller.save(event)
  elif action == 'delete':
    controller.delete()
    return HttpResponseRedirect('/dashboard/event/%s/presenters/add/' % event.id)

  return render_to_response('dashboard/presentation.html', {'form': controller.form, 'form_url': request.META['PATH_INFO'], 'event': event, 'action': action}, 
                            context_instance = RequestContext(request))
  
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
  
