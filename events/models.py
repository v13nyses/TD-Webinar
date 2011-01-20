from django.db import models

# Event model
class Event(models.Model):
  name = models.CharField(max_length = 200)
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()
  tagline = models.CharField(max_length = 1024, blank = True)
  description = models.TextField()
  image = models.ImageField(upload_to = 'events')
  #presentation = models.OneToOneField('presentations.Presentation', blank = True)

  def __unicode__(self):
    return self.name
