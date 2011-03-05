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

from events.forms import LoginForm, LogoutForm, RecommendForm, QuestionForm
from userprofiles.forms import UserProfileForm
from registration.forms import RegisterEventForm

from reporting.models import Engagement, Block
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
#   event/<event_id>/register
def register(request, event_id = None, message = None):
  # if message is None or message == ""
  if not message:
    message = None
  return event(request, event_id, 'pre', 'register.html', message)

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
    
def engagement(request, event_id, seconds):
  current_time = datetime.now()
  seconds = int(seconds)

  if user_is_logged_in(request) and not event_id is None:
    user_profile = UserProfile.objects.get(email = request.session['login_email'])
    event = Event.objects.get(pk = event_id)
    engagements = Engagement.objects.filter(user = user_profile, event = event)

    if len(engagements) == 0:
      engagement = Engagement()
      engagement.user = user_profile
      engagement.event = event
      engagement.ip_address = request.META['REMOTE_ADDR']
      engagement.save()
      start_new_block(engagement, current_time, seconds)
    elif len(engagements) == 1:
      blocks = Block.objects.filter(engagement = engagements[0]).order_by('-start')
      
      if len(blocks) == 0:
        start_new_block(engagement[0], current_time, seconds)
      else:
        # if there is already a block contiguous to the current time
        # if start_time + seconds_already_in_block + seconds_to_be_added + 1(for safety) >= current_time
        delta = current_time - blocks[0].start
        seconds_delta = delta.seconds - blocks[0].seconds - seconds - 1
        if seconds_delta <= 0:
          blocks[0].seconds += seconds
          blocks[0].save()
        else:
          start_new_block(engagements[0], current_time, seconds)
    else:
      # log that something is incorrect, as there is more than one engagement record
      # for a user-event
      pass

  print "done angegement"
  return HttpResponse("engagement view donezors")

def start_new_block(engagement, start_time, seconds):      
  block = Block()
  block.engagement = engagement
  block.start = start_time
  block.seconds = seconds
  block.save()


# used by urls:
#   event/browser-check
def browser_check(request):
  return render_to_response('browser_check.html', {}, context_instance = RequestContext(request))

# used by urls:
#   event/
#   event/<event_id>/
def event(request, event_id = None, state = None, template = 'event.html', user_message = None):
  if request.session.has_key('login_email'):
    print request.session['login_email']
  else:
    print "no login email"
    request.session['login_email'] = None
    request.session['user_registered'] = None

  request.session['thank_you'] = None
  push_analytics = []
  # if we didn't get an event id, grab the newest event
  event = None

  if event_id == None:
    try:
      event = Event.objects.order_by('-live_start_date')[0]
    except IndexError:
      # create a blank event if there aren't any yet
      event = Event()
  else:
    event = Event.objects.get(id = event_id)

  if state == 'debug':
    state = None
    event.debug()
  elif state == 'live':
    if user_is_logged_in(request):
      profile = UserProfile.objects.get(email = request.session['login_email'])
      registration = Registration.objects.get(user_profile = profile)
      if not registration.viewed_live:
        registration.viewed_live = True
        view_event_live(event, profile)
        registration.save()

    event.debug = False

  if state == None:
    state = event.state

  request.session['event_id'] = event.id
  
  if not request.session['login_email'] is None:
    try:
      print "getting reg"
      profile = UserProfile.objects.get(email = request.session['login_email'])
      print profile
      reg = Registration.objects.filter(user_profile = profile, event=event)
      print reg

      if len(reg) == 0:
        print "reg len = 0"
        request.session['user_registered'] = None
      else:
        print "reg found!"
        request.session['user_registered'] = "True"
        if reg[0].completed_exit_survey == "True":
          request.session['thank_you'] = "thanks"
    except UserProfile.DoesNotExist:
      request.session['user_registered'] = None

  if request.GET.has_key('partnerref'):
    push_analytics.append(['_setCustomVar', 2, 'ReferralCode', request.GET['partnerref'], 1])
    push_analytics.append(['_trackEvent', 'Referrals', 'ReferralCode'])

  if request.method == "POST":
    login_form = LoginForm(request.POST)
    logout_form = LogoutForm(request.POST)
    register_event_form = RegisterEventForm(request.POST)
    user_profile_form = UserProfileForm(request.POST)
    recommend_form = RecommendForm(request.POST)

    if user_profile_form.is_valid():
      if not user_profile_exists(user_profile_form.cleaned_data['email']):
        print "new account"
        usr = user_profile_form.save(commit=False)
        usr.ip_address = request.META['REMOTE_ADDR']
        usr.save()
        login_user(user_profile_form.cleaned_data['email'], request)
        register_user_for_event(request)
        push_analytics.append(['_setCustomVar', 1, 'UserEmail', request.session['login_email'], 1])
        push_analytics.append(['_trackEvent', 'Conversions', 'UserEmail'])
        return HttpResponseRedirect(reverse('event', args=[event_id]))
      else:
        # the user already exists
        # TO DO
        print "alread yhas account"
        user_message = "You already have an account with us.  Please login using that account"
    elif login_form.is_valid():
      if user_profile_exists(login_form.cleaned_data['email']):
        login_user(login_form.cleaned_data['email'], request)
        push_analytics.append(['_setCustomVar', 1, 'UserEmail', request.session['login_email'], 1])
        push_analytics.append(['_trackEvent', 'Conversions', 'UserEmail'])
        #if is_first_redirect(request):
        #  return HttpResponseRedirect(reverse('register', args=[event_id, settings.REGISTRATION_MESSAGE]))
        #else:
        return HttpResponseRedirect(reverse('event', args=[event_id]))
      else:
        # Do Nothing (page will reload with no one logged in)
        pass
    elif logout_form.is_valid():
      logout_user(request)

    if recommend_form.is_valid() and user_is_logged_in(request):
      user_profile = UserProfile.objects.get(email = request.session['login_email'])
      message_context = {
        'event': event,
        'from': request.session['login_email'],
      }
      html_message = render_to_string('events/recommend_email.html', message_context)
      text_message = render_to_string('events/recommend_email.txt', message_context)
      email = EmailMultiAlternatives(
        settings.RECOMMEND_EMAIL_SUBJECT.format(profile = user_profile),
        text_message,
        user_profile.email,
        [recommend_form.cleaned_data['to_list']],
      )
      email.attach_alternative(html_message, 'text/html')
      email.send()

    elif register_event_form.is_valid():
      if user_is_logged_in(request):
        register_user_for_event(request)
        user_message = settings.REGISTRATION_MESSAGE
    

  if user_is_logged_in(request):
    push_analytics.append(['_setCustomVar', 1, 'UserEmail', request.session['login_email'], 1])
    push_analytics.append(['_trackEvent', 'Conversions', 'UserEmail'])
    message = settings.REGISTRATION_MESSAGE
    if request.session['user_registered'] is None and is_first_redirect(request):
      print "redirect to register b/c user isn't registered"
      return HttpResponseRedirect(reverse('register', args=[event_id]))
 
  if len(push_analytics) == 0:
    push_analytics = None

  json_analytics = []
  if push_analytics:
    for analytic_call in push_analytics:
      json_analytics.append(json.dumps(analytic_call))

  context_data = {
    'event': event,
    'state': state,
    'stateOffsets': event.state_offsets,
    'login_form': LoginForm(),
    'logout_form': LogoutForm(),
    'register_event_form': RegisterEventForm(),
    'user_profile_form': UserProfileForm(),
    'recommend_form': RecommendForm(),
    'custom_variables': json_analytics,
    'message': user_message
  }

  print "render to response %s" % template
  return render_to_response(template, context_data, context_instance = RequestContext(request))

def is_first_redirect(request):
  print "enter:%s" % request.session['first_redirect']
  if request.session.has_key("first_redirect"):
    if request.session['first_redirect'] != "True":
      print "leave:%s" % request.session['first_redirect']
      return False
    elif request.session['first_redirect'] == "True":
      request.session['first_redirect'] = "False"
  else:
    request.session['first_redirect'] = "True"

  print "leave:%s" % request.session['first_redirect']
  return True

def user_profile_exists(email):
  user = UserProfile.objects.filter(email=email)

  if len(user) >= 1:
    return True

  return False

def login_user(email, request):
  request.session['login_email'] = email

def user_is_logged_in(request):
  return request.session.has_key('login_email') and not request.session['login_email'] is None

def logout_user(request):
  request.session['login_email'] = None
  request.session['user_registered'] = None

def register_user_for_event(request):
  profile = UserProfile.objects.get(email = request.session['login_email'])
  registration = Registration.objects.filter(user_profile=profile, event=request.session['event_id'])

  if len(registration) == 0:
    registration = Registration()
    registration.user_profile = profile
    registration.event = Event.objects.get(id=request.session['event_id'])
    registration.ip_address = request.META['REMOTE_ADDR']
    registration.save()

  request.session['user_registered'] = "True"

def presentation(request, event_id, state = None):
  event = Event.objects.get(id = event_id)
  if state == None:
    state = event.state

  template = 'events/presentation_%s.html' % state
  
  return render_to_response([template, 'events/presentation.html'], {'event': event, 'state': state}, context_instance = RequestContext(request))
