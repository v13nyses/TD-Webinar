from django.db import models
from django.conf import settings
from datetime import datetime, timedelta
from pytz import timezone
from django.utils.text import truncate_words
from django.template.defaultfilters import slugify

# setup some helper functions to find the upload paths at runtime
def event_upload_base_path(event):
  # truncate the event name and turn it into a valid url
  event_slug = slugify(truncate_words(event.name, settings.EVENT_SLUG_WORDS))

  return "events/%s" % (event_slug)

def event_upload_to(event, filename):
  return "%s/%s" % (event_upload_base_path(event), filename)

# Event model
class Event(models.Model):
  name = models.CharField(max_length = 200)
  short_description = models.TextField()
  description = models.TextField()
  image = models.ImageField(upload_to = event_upload_to)
  resource_guide = models.FileField(upload_to = event_upload_to)
  lobby_video = models.OneToOneField('presentations.Video', blank = True, null = True)
  presentation = models.OneToOneField('presentations.Presentation', blank = True, null = True)

  # these dates are used to find the current state of the event
  lobby_start_date = models.DateTimeField()
  live_start_date = models.DateTimeField()
  live_stop_date = models.DateTimeField()
  archive_start_date = models.DateTimeField()

  debug = False

  def live_offset(self, time_delta):
    lobby_start_date = self.lobby_start_date.replace(tzinfo = timezone(settings.TIME_ZONE))

    return lobby_start_date + time_delta
    
  def time_difference(self, time_a, time_b = None):
    """ Returns time_a - time_b in seconds. If time_a < time_b, returns -1. """
    if time_b == None:
      time_b = datetime.now(timezone(settings.TIME_ZONE))

    # make sure both times have the correct timezone
    time_a = time_a.replace(tzinfo = timezone(settings.TIME_ZONE))
    time_b = time_b.replace(tzinfo = timezone(settings.TIME_ZONE))

    if time_a < time_b:
      return -1

    return (time_a - time_b).seconds
    
  def debug(self):
    self.debug = True

    now = datetime.now(timezone(settings.TIME_ZONE))
    self.lobby_start_date = now + timedelta(seconds = 10)
    self.live_start_date = now + timedelta(seconds = 20)
    self.live_stop_date = now + timedelta(seconds = 50)
    self.archive_start_date = now + timedelta(seconds = 60)
    self.save()

  def get_state(self):
    # grab the current date, and add timezone info to all our date fields
    now = datetime.now(timezone(settings.TIME_ZONE))
    lobby_start_date = self.lobby_start_date.replace(tzinfo = timezone(settings.TIME_ZONE))
    live_start_date = self.live_start_date.replace(tzinfo = timezone(settings.TIME_ZONE))
    live_stop_date = self.live_stop_date.replace(tzinfo = timezone(settings.TIME_ZONE))
    archive_start_date = self.archive_start_date.replace(tzinfo = timezone(settings.TIME_ZONE))

    # using the current time, find out the state of the event
    if now < lobby_start_date:
      return self.STATE_PRE
    elif now < live_start_date:
      return self.STATE_LOBBY
    elif now < live_stop_date:
      return self.STATE_LIVE
    elif now < archive_start_date:
      return self.STATE_POST
    else:
      return self.STATE_ARCHIVE

  def get_start_offset(self):
    # only calculate an offset for live events, return 0 for everything else
    if self.state == self.STATE_LIVE:
      now = datetime.now(timezone(settings.TIME_ZONE))
      live_start_date = self.live_start_date.replace(tzinfo = timezone(settings.TIME_ZONE))

      return (now - live_start_date).seconds

    else:
      return 0

  def get_presenters(self):
    # build a special array of presenters for use in templates
    presenter_types = {}

    for presenter in self.presentation.presenters.all():
      if not presenter_types.has_key(presenter.presenter_type):
        presenter_types[presenter.presenter_type] = {
            'type': presenter.presenter_type,
            'presenters': []
        }

      presenter_types[presenter.presenter_type]['presenters'].append(presenter)

    # because of annoying limitations in the template for tag, we need to return an array, not a dict
    presenter_types_list = []
    for presenter_type in presenter_types:
      presenter_types_list.append(presenter_types[presenter_type])

    return presenter_types_list

  def get_state_offsets_debug(self):
    return {
        'lobby': 10,
        'live': 20,
        'post': 50,
        'archive': 60
    }

  def get_state_offsets(self):
    if self.debug:
      return self.get_state_offsets_debug()

    return {
        'lobby': self.time_difference(self.lobby_start_date),
        'live': self.time_difference(self.live_start_date),
        'post': self.time_difference(self.live_stop_date),
        'archive': self.time_difference(self.archive_start_date)
    }

  def __unicode__(self):
    return self.name

  state = property(get_state, doc = 'The current state of the event.')
  start_offset = property(get_start_offset, doc = 'The number of seconds the event has been live.')
  presenters = property(get_presenters, doc = 'A special array of presenters for use in templates.')
  state_offsets = property(get_state_offsets)

  STATE_PRE = 'pre' 
  STATE_LOBBY = 'lobby'
  STATE_LIVE = 'live'
  STATE_POST = 'post'
  STATE_ARCHIVE = 'archive'

  class Meta:
    permissions = (
      ("can_view_dashboard", "Can view event dashboard"),
    )
