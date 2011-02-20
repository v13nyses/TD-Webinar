from django.db import models
from 

# Create your models here.
class Question(models.Model):
  question = models.CharField(max_length=255)

  def __unicode__(self):
    return self.question

class Result(models.Model):
  result_type = models.ForeignKey('ResultType')
  question = models.ForeignKey('Question')

  def __unicode__(self):
    return "%s - %s " % (self.question, self.result_type)

class ResultType(PolyModel):
  pass
  #name = models.CharField(max_length=200)

  def __unicode__(self):
    return ""

class ChooseOne(ResultType):
  value = models.CharField(max_length=200)
  votes = models.IntegerField()

  def __unicode__(self):
    return "%s: %d" % (self.value, self.votes)

class ChooseMany(ResultType):
  value = models.CharField(max_length=200)
  votes = models.IntegerField()

  def __unicode__(self):
    return "%s: %d" % (self.value, self.votes)
