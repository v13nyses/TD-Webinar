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
      event = Event()

  else:
    try:
      event = Event.objects.get(id = event_id)
    except Event.DoesNotExist:
      event = Event()

  # try and load the video
  try:
    event.video_id = event.presentation_set.get().video_set.get().video_id
    event.presentation_id = event.presentation_set.get().id
    
    # add timezones to everything to make sure the dates match
    now = datetime.now(timezone(settings.TIMEZONE))
    start_date = event.start_date.replace(tzinfo = timezone(settings.TIMEZONE))
    event.start_offset = (now - start_date).seconds

    print now
    print start_date
    print event.start_offset

  except:
    event.video_id = ''
    event.presentation_id = ''
    event.start_offset = 0

  return render_to_response('event.html', {'event': event}, 
                            context_instance = RequestContext(request))
