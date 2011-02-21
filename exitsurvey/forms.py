from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
import ipdb

from exitsurvey.models import ExitQuestion, ExitResult
from exitsurvey.models import CHOOSE_ONE, CHOOSE_MANY, COMMENT, COMMENT_REQUIRED

def make_exit_survey_form(questions):
  fields = {}
  for question in questions:
    results = question.exitresult_set.all().order_by('number')

    if len(results) > 0:
      result_choices = []
      for n in results:
        if n.result_type == CHOOSE_ONE or n.result_type == CHOOSE_MANY:
          result_choices.append([n.id, n.answer])
      
      result_type_flag = False
      results = question.exitresult_set.all().order_by('number')
      for n in results:
        if n.result_type == CHOOSE_ONE and not result_type_flag:
          result_type_flag = True
          fields['%s' % question.id] = forms.ChoiceField(label = question.question,
            choices = result_choices, widget=forms.RadioSelect(choices=result_choices))
        elif n.result_type == CHOOSE_MANY and not result_type_flag:
          result_type_flag = True
          fields['%s' % question.id] = forms.MultipleChoiceField(label = question.question,
            choices = result_choices,
            widget=forms.CheckboxSelectMultiple(choices = result_choices))
        elif n.result_type == COMMENT:
          fields['_%s' % question.id] = forms.CharField(required=False,
            label = "Comment",
            widget=forms.TextInput)
        elif n.result_type == COMMENT_REQUIRED:
          fields['_%s' % question.id] = forms.CharField(widget=forms.TextInput,
            label = "Comment")
             
      
  return type('ExitSurveyForm', (forms.BaseForm,), { 'base_fields': fields })
