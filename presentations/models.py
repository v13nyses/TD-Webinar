from django.db import models
#from foobar.events import Event


# Presentation model
class Presentation(models.Model):
  #video = models.OneToOneField('videos.Video')
  presenters = models.ManyToManyField('Presenter')
  event = models.ForeignKey('events.Event')

class QueuePoint(models.Model):
  slide = models.OneToOneField('Slide')
  time_offset = models.IntegerField()
  presentation = models.ForeignKey('Presentation')

  def __unicode__(self):
    return self.name

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

class Slide(models.Model):
  image = models.ImageField(upload_to = 'slides')
  presentation = models.ForeignKey('Presentation')

class Video(models.Model):
  video_id = models.IntegerField()
  presentation = models.ForeignKey('Presentation')
