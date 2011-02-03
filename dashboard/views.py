from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from form_controllers import EventFormController, PresentationFormController
from events.models import Event
from presentations.models import Presenter

# used by urls:
#   dashboard/event/add/
#   dashboard/event/<event_id>/
#   dashboard/
def event(request, event_id = None, action = 'add'):
  if event_id != None:
    event = Event.objects.get(id = event_id)
    controller = EventFormController(request, event)
  else: 
    controller = EventFormController(request)

  if controller.save() and (action == 'add' or action == 'edit'):
    id = controller.form.instance.id
    return HttpResponseRedirect(reverse('db_presenter_add', args=[id]))

  return render_to_response('dashboard/event.html', {'form': controller.form, 'action': action, 'event': controller.form.instance}, 
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
#   dashboard/<event_id>/presenters/add
#   dashboard/<event_id>/presenter/<presenter_id>/
def presenter(request, event_id = None, presenter_id = None, action = 'add'):
  if presenter_id == None:
    presenter = Presenter()
  else:
    presenter = Presenter.objects.get(id = presenter_id)

  event = Event.objects.get(id = event_id)
  controller = PresentationFormController(request, instance = presenter)

  if action == 'add':
    controller.save(event)
  elif action == 'delete':
    controller.delete()
    return HttpResponseRedirect('/dashboard/event/%s/presenters/add/' % event.id)

  return render_to_response('dashboard/presentation.html', {'form': controller.form, 'event': event, 'action': action, 'presenter': presenter}, 
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
  
