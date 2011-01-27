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
    end_date = event.end_date.replace(tzinfo = timezone(settings.TIMEZONE))
    event.start_offset = (now - start_date).seconds

    print "!!! Now: %s" % now
    print "!!! Start date: %s" % start_date
    print "!!! End date: %s" % end_date
    print "!!! diff: %d" % (end_date - start_date).seconds
    print "!!! start_offset: %d" % event.start_offset

    if now < start_date:
      event.state = 'pre'
    elif now > end_date:
      event.state = 'post'
    else:
      event.state = 'live'

  except:
    event.video_id = ''
    event.presentation_id = ''
    event.start_offset = 0

  presenters = build_presenters(event)

  return render_to_response('event.html', {'event': event, 'presenters': presenters}, 
                            context_instance = RequestContext(request))

def build_presenters(event):
  presenter_types = {}

  for presenter in event.presentation_set.get().presenters.all():
    try:
      presenter_types[presenter.presenter_type]['presenters'].append(presenter)
    
    except KeyError:
      presenter_types[presenter.presenter_type] = {'type': presenter.presenter_type, 'presenters': []}
      presenter_types[presenter.presenter_type]['presenters'].append(presenter)

  # because of annoying limitations in the template for tag, we need to return an array, not a dict
  presenter_types_list = []
  for presenter_type in presenter_types:
    presenter_types_list.append(presenter_types[presenter_type])

  return presenter_types_list
