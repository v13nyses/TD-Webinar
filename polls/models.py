from django.db import models
from presentations.models import Slide

# Create your models here.
class Poll(Slide):
  question = models.CharField(max_length=200)

  def __unicode__(self):
    return "%s (Poll %s)" % (super(Poll, self).__unicode__(), self.question)

class Choice(models.Model):
  poll = models.ForeignKey('Poll')
  choice = models.CharField(max_length=200)
  votes = models.IntegerField()

  def __unicode__(self):
    return "%s (Choice %s)" % (self.poll.__unicode__(), self.choice)
