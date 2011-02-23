from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple, Input
import ipdb
import string
import re

from exitsurvey.models import ExitQuestion, ExitResult
from exitsurvey.models import CHOOSE_ONE, CHOOSE_MANY, COMMENT, COMMENT_REQUIRED

def make_exit_survey_form(questions):
  fields = {}
  current_section = None
  for question in questions:
    results = question.exitresult_set.all().order_by('number')

    if current_section != question.section:
      current_section = question.section
      fields['%s-0' % question.id] = forms.BooleanField(label = current_section.name,
        widget=LabelWidget,
        required=False)

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
          fields['%s-1' % question.id] = forms.ChoiceField(label = question.question,
            choices = result_choices, widget=forms.RadioSelect(choices=result_choices))
        elif n.result_type == CHOOSE_MANY and not result_type_flag:
          result_type_flag = True
          fields['%s-1' % question.id] = forms.MultipleChoiceField(label = question.question,
            choices = result_choices,
            widget=forms.CheckboxSelectMultiple(choices = result_choices))
        elif n.result_type == COMMENT:
          fields['%s-1-%d' % (question.id, n.number)] = forms.CharField(required=False,
            label = n.label,
            widget=forms.Textarea)
        elif n.result_type == COMMENT_REQUIRED:
          fields['%s-1-%d' % (question.id, n.number)] = forms.CharField(widget=forms.Textarea,
            label = n.label)
             
  return type('ExitSurveyForm', (forms.BaseForm,), { 'base_fields': fields })


class LabelWidget(Input):
  def render(self, name, value, attrs=None):
    html_out = super(LabelWidget, self).render(name, value, attrs)
    html_out = string.replace(html_out, 'input', 'div class="section-label"')
    split_html = re.split('type="(\w+)"', html_out)
    if len(split_html) == 3:
      html_out = split_html[0] + split_html[2]
    return html_out
