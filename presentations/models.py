from django.db import models
#from foobar.events import Event
from django.shortcuts import render_to_response
from django.template import RequestContext
from snippetscream import PolyModel
from events.models import event_upload_base_path
from django.conf import settings

def slide_upload_to(slide, filename):
  event = slide.slide_set.presentation.event
  return "%s/slides/%s" % (event_upload_base_path(event), filename)

# Presentation model
class Presentation(models.Model):
  video = models.OneToOneField('Video', blank = True, null = True)
  presenters = models.ManyToManyField('Presenter', blank = True, null = True)
  slide_set = models.OneToOneField('SlideSet', blank = True, null = True)

  def __unicode__(self):
    return 'Presentation: %d' % (self.id)

class Presenter(models.Model):
  name = models.CharField(max_length = 200)
  description = models.TextField(blank = True)
  job_title = models.CharField(max_length = 100)
  photo = models.ImageField(upload_to = 'presenters', blank = True)
  presenter_type = models.ForeignKey('PresenterType')

  def __unicode__(self):
    return self.name

class PresenterType(models.Model):
  name = models.CharField(max_length = 200)

  def __unicode__(self):
    return self.name

class Slide(PolyModel):
  image = models.ImageField(upload_to = slide_upload_to)
  slide_set = models.ForeignKey('SlideSet')
  offset = models.IntegerField()

  def __unicode__(self):
    return '%s (Slide %d)' % (self.slide_set.__unicode__(), self.id)

  def display(self, request, slide):
    return render_to_response('presentations/slide.html', {'slide': slide, 'settings': settings},
      context_instance = RequestContext(request))

class SlideSet(models.Model):
  changed = models.BooleanField(default="true",editable=False)
  export_pdf = models.FileField(upload_to='slidesets',editable=False)

  def __unicode__(self):
    return "SlideSet %d" % (self.id)

  def export_pdf(self):
    # TO DO
    pass

  def import_pdf(self, pdf_file):
    # TO DO
    pass

  def get_ordered_slides(self):
    # TO DO
    pass

class Video(models.Model):
  video_id = models.CharField(max_length=50)
  player_id = models.CharField(max_length=50)
  archive_player_id = models.CharField(max_length=50, blank = True)

  def get_archive_url(self):
    if self.archive_player_id:
      return settings.VIDEO_URL % (self.video_id, self.archive_player_id)
    else:
      return self.url

  def get_url(self):
    return settings.VIDEO_URL % (self.video_id, self.player_id)

  url = property(get_url, doc = "The url of the javascript used to load the video.")
  archive_url = property(get_archive_url, doc = "The url of the javascript used to load the video.")

  def __unicode__(self):
    return 'Video: %s (Player: %s, id: %d)' % (self.video_id, self.player_id, self.id)
