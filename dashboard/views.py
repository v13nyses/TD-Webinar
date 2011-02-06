from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from form_controllers import EventFormController, PresentationFormController, SlideFormController
from events.models import Event
from presentations.models import Presenter, Slide
import ipdb

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
#   dashboard/event/<event_id>/slide/<slide_id>/<action> 
def slide(request, event_id, slide_id = None, action = 'add'):
  event = Event.objects.get(id = event_id)

  if slide_id != None:
    slide = Slide.objects.get(id = slide_id)
    controller = SlideFormController(request, event, slide)

  else:
    controller = SlideFormController(request, event)

  controller.set_action(action)

  if request.POST.has_key('submit') and request.POST['submit'].find('Back') != -1:
    return HttpResponseRedirect(reverse('db_presenter_add', args=[event.id]))

  if action == 'add' or action == 'edit':
    if controller.save() and request.POST.has_key('submit'):
      if request.POST['submit'].find('Continue') != -1:
        pass
        #return HttpResponseRedirect(reverse('db_slide_add', args=[event.id]))
  elif action == 'delete':
    controller.delete()
    return HttpResponseRedirect(reverse('db_slide_add', args=[event.id]))
  return render_to_response('dashboard/slides.html', {'form': controller.form, 'action': action, 'slide': controller.form.instance, 'event': event}, 
                            context_instance = RequestContext(request))

  
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
  controller.set_action(action, presenter)

  if request.POST.has_key('submit') and request.POST['submit'].find('Back') != -1:
    return HttpResponseRedirect(reverse('db_event_edit', args=[event.id]))

  if action == 'add' or action == 'edit':
    if controller.save(event) and request.POST.has_key('submit'):
      if request.POST['submit'].find('Continue') != -1:
        return HttpResponseRedirect(reverse('db_slide_add', args=[event.id]))
  elif action == 'delete':
    controller.delete()
    return HttpResponseRedirect(reverse('db_presenter_add', args=[event.id]))

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
  
