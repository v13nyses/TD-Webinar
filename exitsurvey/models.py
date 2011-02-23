from django.db import models
from snippetscream import PolyModel

#from events.models import Event

CHOOSE_ONE = "choose_one"
CHOOSE_MANY = "choose_many"
COMMENT = "comment"
COMMENT_REQUIRED = "comment_required"


class ExitSection(models.Model):
  name = models.CharField(max_length=200)

  def __unicode__(self):
    return "ExitSection: %s" % self.name

# Create your models here.
class ExitQuestion(models.Model):
  question = models.CharField(max_length=255)
  event = models.ForeignKey('events.Event') 
  section = models.ForeignKey('ExitSection')
  number = models.IntegerField()

  def __unicode__(self):
    return "ExitQuestion %d: %s" % (self.number, self.question)

class ExitResult(models.Model):
  #result_type = models.ForeignKey('ExitResultType')
  result_type = models.CharField(max_length=200)
  question = models.ForeignKey('ExitQuestion')
  answer = models.CharField(max_length=500, blank=True)
  label = models.CharField(max_length=200, blank=True)
  results = models.IntegerField(default=0)
  number = models.IntegerField()

  def __unicode__(self):
    return "ExitResult %d: %s (%s)" % (self.number, self.answer, self.result_type)

#class ExitResultType(models.Model):
#  name = models.CharField(max_length=200)
