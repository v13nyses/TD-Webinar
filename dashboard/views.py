from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from form_controllers import FormController, EventFormController, PresentationFormController, SlideFormController
from events.models import Event
from events.views import logout_user
from presentations.models import Presenter, Slide

# used by urls:
#   dashboard/event/add/
#   dashboard/event/<event_id>/
#   dashboard/
def event(request, event_id = None, action = 'add'):
  if event_id != None:
    event = Event.objects.get(id = event_id)
    controller = EventFormController(request, event)
    continue_button = True
    redirect = controller.submit(continue_path = reverse('db_presenter_add', args = [event.id]),
                                 back_path = reverse('db_dashboard'))
  else: 
    controller = EventFormController(request)
    continue_button = False
    redirect = controller.submit(back_path = reverse('db_dashboard'))


  if redirect:
    return HttpResponseRedirect(redirect)

  return render_to_response('dashboard/event.html', {'form': controller.form, 'action': action, 'event': controller.form.instance, 'continue_button': continue_button}, 
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

  if action == 'delete':
    controller.delete()
    return HttpResponseRedirect(reverse('db_slide_add', args=[event.id]))

  controller.set_action(action)
  redirect = controller.submit(continue_path = reverse('db_preview', args = [event.id]),
                               back_path = reverse('db_presenter_add', args = [event.id]))
  if redirect:
    return HttpResponseRedirect(redirect)

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
  controller = PresentationFormController(request, event, instance = presenter)

  if action == 'delete':
    controller.delete()
    return HttpResponseRedirect(reverse('db_presenter_add', args=[event.id]))

  controller.set_action(action, presenter)
  redirect = controller.submit(continue_path = reverse('db_slide_add', args = [event.id]),
                               back_path = reverse('db_event_edit', args = [event.id]))
  if redirect:
    return HttpResponseRedirect(redirect)

  return render_to_response('dashboard/presentation.html', {'form': controller.form, 'event': event, 'action': action, 'presenter': presenter}, 
                            context_instance = RequestContext(request))
  
def preview(request, event_id, state = 'pre'):
  event = Event.objects.get(id = event_id)
  controller = FormController(request)

  redirect = controller.submit(continue_path = reverse('event', args = [event.id]),
                               back_path = reverse('db_slide_add', args = [event.id]))
  if redirect:
    return HttpResponseRedirect(redirect)

  context = {
    'event': event,
    'state': state
  }
  context_instance = RequestContext(request)

  logout_user(request)

  return render_to_response('dashboard/preview.html', context, context_instance)

def dashboard(request):
  events = Event.objects.order_by('live_start_date')

  context = {
    'events': events
  }
  context_instance = RequestContext(request)
  return render_to_response('dashboard/dashboard.html', context, context_instance)
