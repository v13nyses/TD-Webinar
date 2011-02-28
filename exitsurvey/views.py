from exitsurvey.models import ExitQuestion, ExitResult
from exitsurvey.forms import make_exit_survey_form
from exitsurvey.models import CHOOSE_ONE, CHOOSE_MANY, COMMENT, COMMENT_REQUIRED
from events.models import Event
from userprofiles.models import UserProfile
from registration.models import Registration
from events.views import user_is_logged_in

from django import forms
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.conf import settings
import simplejson as json
import ipdb


# Create your views here.
def thank_you(request, event_id = None):
  return render_to_response('exitsurvey/thank_you.html',
      {}, context_instance = RequestContext(request))

def exit_survey(request, event_id = None):
  if request.session.has_key('login_email'):
    if not user_is_logged_in(request):
      return HttpResponseRedirect(reverse('register', args=[event_id]))

    profile = UserProfile.objects.get(email = request.session['login_email'])
    registrations = Registration.objects.filter(event = event_id, user_profile = profile)
    if len(registrations) == 1:
      reg = registrations[0]
      #ipdb.set_trace()
      if reg.completed_exit_survey == "True":
        return HttpResponseRedirect(reverse('thank_you', args=[event_id]))
    else:
      return HttpResponseRedirect(reverse('register', args=[event_id]))
  else:
    return HttpResponseRedirect(reverse('register', args=[event_id]))

  exit_questions = ExitQuestion.objects.filter(
      event=Event.objects.get(pk=event_id)
    ).order_by('number')
  exit_survey = make_exit_survey_form(exit_questions)(request.POST or None)
  #
  # if this doesn't work to order the form fields be sure to check that 
  # django.forms.forms.BaseForm.as_p() is using self.fields.items() to generate
  # the form html
  #
  # perform mad hax
  exit_survey.fields = SpecialDict(exit_survey.fields)
  # ??
  # PROFIT!!

  if request.method == "POST":
    if exit_survey.is_valid():

      for question in exit_questions:
        results = question.exitresult_set.all()
        result_choose_flag = False
        result_list = []

        for n in results:
          if not result_choose_flag:
            if n.result_type == CHOOSE_ONE or n.result_type == CHOOSE_MANY: 
              aoeu = exit_survey.cleaned_data['%s-1' % question.id]
              if isinstance(aoeu, list):
                result_list = result_list + aoeu
              else:
                result_list.append(aoeu)
              result_choose_flag = True
          elif n.result_type == COMMENT:
              aoeu = exit_survey.cleaned_data['%s-1-%d' % (question.id, n.number)]
              if isinstance(aoeu, list):
                result_list = result_list + aoeu
              else:
                result_list.append(aoeu)

        for r in result_list:
          try:
            result = ExitResult.objects.get(pk=r)
            if result.result_type == CHOOSE_ONE or result.result_type == CHOOSE_MANY:
              result.results = result.results + 1
              result.save()
          except ValueError:
            if not r == '':
              new_result = ExitResult()
              new_result.question = question
              new_result.result_type = COMMENT
              new_result.number = 999
              new_result.results = 1
              new_result.answer = r
              new_result.save()

      reg.completed_exit_survey = "True"
      reg.save()
      return HttpResponseRedirect(reverse('thank_you', args=[event_id]))
    

  context_data = {
    'exit_survey': exit_survey,
  }

  return render_to_response('exitsurvey/survey.html',
    context_data, context_instance = RequestContext(request))


class SpecialDict(dict):
  def __init__(self, a_dict):
    super(SpecialDict, self).__init__(a_dict)

  def items(self):
    item_list = super(SpecialDict, self).items()
    item_list.sort(cmp=my_comp)
    return item_list


def my_comp(item1, item2):
  if isinstance(item1, tuple) and isinstance(item2, tuple):
    if item1[0] < item2[0]:
      return -1
    elif item1[0] > item2[0]:
      return 1

  return 0
