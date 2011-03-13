from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.template.loader import render_to_string
from django.conf import settings
from django.template.defaultfilters import slugify
from events.models import Event, Question
from dashboard.utils import presentation_to_pdf
from presentations.models import slide_upload_to
from datetime import datetime
from pytz import timezone
import os
import logging
from django.core.mail import EmailMessage, EmailMultiAlternatives

from events.forms import RecommendForm, QuestionForm

from registration.models import Registration
from userprofiles.models import UserProfile
from eventmailer.models import view_event_live
import simplejson as json
import ipdb

try:
  from mailer import send_mail
except ImportError:
  from django.core.mail import send_mail

logger = logging.getLogger(__name__)


# used by urls:
#   event/<event_id>/slides/
def slides(request):
  # TO DO
  pass

# used by urls:
#   event/<event_id>/<filename>.pdf
def pdf(request, event_id = None):
  event = Event.objects.get(id = event_id)
  logger.info("Requesting PDF for '%s' (%d), presentation_pdf = %s" %
      (event.name, event.id, event.presentation_pdf))
  if event.presentation_pdf == '' or \
     not os.path.exists(os.path.join(settings.MEDIA_ROOT, event.presentation_pdf.path)):
    # grab a list of slides from the presentation
    slide = event.presentation.slide_set.slide_set.order_by("offset")[0]
    pdf_path = slide_upload_to(slide, event.slug + ".pdf")
    pdf_full_path = os.path.join(settings.MEDIA_ROOT, pdf_path)
    result = presentation_to_pdf(event.presentation, pdf_full_path)
    if result == 0:
      logger.info("Conversion successful")
    else:
      logger.info("Error converting to pdf: %d" % result)

    event.presentation_pdf = pdf_path
    event.save()

  return HttpResponseRedirect("%s%s" % (settings.MEDIA_URL, event.presentation_pdf))

# used by urls:
#   event/<event_id>/submit_question
def submit_question(request, event_id = None):
  result = False

  if event_id and request.POST:
    question = Question()
    question.event = Event.objects.get(id = event_id)
    question.question = request.POST['question']

    if user_is_logged_in(request):
      profile = UserProfile.objects.get(email = request.session['login_email'])
      question.registration = Registration.objects.get(user_profile = profile)

    question.save()

    logger.info("Question submitted: %s" % question.question)

    result = True

  return HttpResponse(json.dumps({'result': result}), mimetype = 'application/javascript')
    
#   event/browser-check
def browser_check(request):
  return render_to_response('browser_check.html', {}, context_instance = RequestContext(request))

# used by urls:
#   event/
#   event/<event_id>/
def event(request, event_id = None, state = None, user_message = None):
  profile = None
  registration = None
  request.session['thank_you'] = None
  request.session['user_registered'] = None

  # if we didn't get an event id, grab the newest event
  event = get_event(event_id)
  request.session['event_id'] = event.id

  if request.session.has_key('login_email'):
    profile, registration = get_user_profile_registration(event, request.session['login_email'])

    if profile and registration:
      request.session['user_registered'] = "True"
      if registration.completed_exit_survey == "True":
        request.session['thank_you'] = "thanks"
  else:
    request.session['login_email'] = None

  if state == 'debug':
    state = None
    event.debug()
  elif state == 'live':
    if user_is_logged_in(request):
      if registration and not registration.viewed_live:
        registration.viewed_live = True
        view_event_live(event, profile)
        registration.save()

    event.debug = False

  if state == None:
    state = event.state

  #if not request.session['login_email'] is None:
  #  if profile:
  #    if registration:
  #      request.session['user_registered'] = "True"
  #      if registration.completed_exit_survey == "True":
  #        request.session['thank_you'] = "thanks"

  if request.method == "POST":
    recommend_form = RecommendForm(request.POST)

    if recommend_form.is_valid() and user_is_logged_in(request):
      message_context = {
        'event': event,
        'from': request.session['login_email'],
      }
      html_message = render_to_string('events/recommend_email.html', message_context)
      text_message = render_to_string('events/recommend_email.txt', message_context)
      email = EmailMultiAlternatives(
        settings.RECOMMEND_EMAIL_SUBJECT.format(profile = profile),
        text_message,
        profile.email,
        [recommend_form.cleaned_data['to_list']],
      )
      email.attach_alternative(html_message, 'text/html')
      email.send()

  if user_is_logged_in(request):
    if request.session['user_registered'] is None:
      return HttpResponseRedirect(reverse('register', args=[event_id]))
 
  context_data = {
    'event': event,
    'state': state,
    'stateOffsets': event.state_offsets,
    'recommend_form': RecommendForm(),
  }

  return render_to_response('event.html', context_data, context_instance = RequestContext(request))


def get_event(event_id):
  event = None

  if event_id == None:
    try:
      event = Event.objects.order_by('-live_start_date')[0]
    except IndexError:
      # create a blank event if there aren't any yet
      event = Event()
  else:
    event = Event.objects.get(id = event_id)

  return event


def get_user_profile_registration(event, user_email):
  prfl = None
  reg = None

  if user_email:
    prfl = UserProfile.objects.filter(email = user_email)

    if len(prfl) == 1:
      prfl = prfl[0]
    else:
      prfl = None

    reg = Registration.objects.filter(user_profile = prfl, event=event)

    if len(reg) == 1:
      reg = reg[0]
    else:
      reg = None

  return prfl, reg


def user_is_logged_in(request):
  return request.session.has_key('login_email') and not request.session['login_email'] is None


def presentation(request, event_id, state = None):
  event = Event.objects.get(id = event_id)
  if state == None:
    state = event.state

  template = 'events/presentation_%s.html' % state
  
  return render_to_response([template, 'events/presentation.html'], {'event': event, 'state': state}, context_instance = RequestContext(request))
