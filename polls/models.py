from django.db import models
from presentations.models import Slide
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your models here.
class Poll(Slide):
  question = models.CharField(max_length=200)
  
  def __unicode__(self):
    return "%s (Poll %s)" % (super(Poll, self).__unicode__(), self.question)

  def display(self, request, poll):
    try:
      selected_choice = poll.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
      return render_to_response('polls/poll.html', {'poll': poll},
        context_instance = RequestContext(request))
    else:
      selected_choice.votes += 1
      selected_choice.save()
      return render_to_response('polls/poll_as_slide.html', {'poll': poll},
        context_instance = RequestContext(request))

class Choice(models.Model):
  poll = models.ForeignKey('Poll')
  choice = models.CharField(max_length=200)

  def __unicode__(self):
    return "%s (Choice %s)" % (self.poll.__unicode__(), self.choice)

class Vote(models.Model):
  choice = models.ForeignKey('Choice')
  user_profile = models.ForeignKey('userprofiles.UserProfile', blank = True, null = True)
