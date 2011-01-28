from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from events.models import Event
from datetime import datetime
from pytz import timezone

def display(request, event_id = None):
  # if we didn't get an event id, grab the newest event
  if event_id == None:
    try:
      event = Event.objects.order_by('-start_date')[0]
    except IndexError:
      # create a blank event if there aren't any yet
      event = Event()

  else:
    event = Event.objects.get_or_create(id = event_id)

  return render_to_response('event.html', {'event': event}, 
                            context_instance = RequestContext(request))
