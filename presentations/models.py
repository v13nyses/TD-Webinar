from django.db import models
#from foobar.events import Event
from django.shortcuts import render_to_response
from django.template import RequestContext
from snippetscream import PolyModel


# Presentation model
class Presentation(models.Model):
  video = models.OneToOneField('Video')
  presenters = models.ManyToManyField('Presenter')
  slide_set = models.OneToOneField('SlideSet')

  def __unicode__(self):
    return '%s (Presentation)' % (self.event.name)

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
  image = models.ImageField(upload_to = 'slides')
  slide_set = models.ForeignKey('SlideSet')
  offset = models.IntegerField()

  def __unicode__(self):
    return '%s (Slide %d)' % (self.slide_set.__unicode__(), self.id)

  def display(self, request, slide):
    return render_to_response('presentations/slide.html', {'slide': slide},
      context_instance = RequestContext(request))

class SlideSet(models.Model):
  changed = models.BooleanField(default="true",editable=False)
  export_pdf = models.FileField(upload_to='slidesets',editable=False)

  def __unicode__(self):
    return "%s (SlideSet %d)" % (self.presentation.__unicode__(), self.id)

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

  def get_url(self):
    return settings.VIDEO_URL % (video_id, player_id)

  url = property(get_url, doc = "The url of the javascript used to load the video.")

  def __unicode__(self):
    return '%s (Video %d)' % (self.presentation.event.name, self.id)
