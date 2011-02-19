from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.conf import settings
from django.template.defaultfilters import slugify
from events.models import Event, Question
from dashboard.utils import presentation_to_pdf
from presentations.models import slide_upload_to
from datetime import datetime
from pytz import timezone
import os
import logging
from django.core.mail import EmailMessage

from events.forms import LoginForm, LogoutForm, RecommendForm, QuestionForm
from userprofiles.forms import UserProfileForm
from registration.forms import RegisterEventForm

from registration.models import Registration
from userprofiles.models import UserProfile
import simplejson as json

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

  return HttpResponseRedirect("%s/%s" % (settings.MEDIA_URL, event.presentation_pdf))

# used by urls:
#   event/<event_id>/register
def register(request, event_id = None):
  return event(request, event_id, 'pre', 'register.html')

# used by urls:
#   event/<event_id>/submit_question
def submit_question(request, event_id = None):
  result = False

  if event_id and request.POST:
    question = Question()
    question.event = Event.objects.get(id = event_id)
    question.question = request.POST['question']
    question.save()

    result = True

  return HttpResponse(json.dumps({'result': result}), mimetype = 'application/javascript')
    

# used by urls:
#   event/
#   event/<event_id>/
def event(request, event_id = None, state = None, template = 'event.html'):
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
  else:
    event.debug = False

  if not request.session.has_key('was_redirected'):
    request.session['was_redirected'] = "False"

  if request.session['was_redirected'] == "True":
    request.session['was_redirected'] = "False"
  else:
    request.session['first_redirect'] = "True"

  if state == None:
    state = event.state

  request.session['event_id'] = event.id
  
  if not request.session.has_key('login_email'):
    request.session['login_email'] = None
    request.session['user_registered'] = None
  else:
    reg = Registration.objects.filter(email=request.session['login_email']).filter(event=event.id)

    print len(reg)
    if len(reg) == 0:
      request.session['user_registered'] = None
    else:
      request.session['user_registered'] = "True"

  if request.method == "POST":
    print "posting"
    login_form = LoginForm(request.POST)
    logout_form = LogoutForm(request.POST)
    register_event_form = RegisterEventForm(request.POST)
    user_profile_form = UserProfileForm(request.POST)
    recommend_form = RecommendForm(request.POST)

    if user_profile_form.is_valid():
      if not user_profile_exists(user_profile_form.cleaned_data['email']):
        user_profile_form.save()
        login_user(user_profile_form.cleaned_data['email'], request)
        register_user_for_event(request)
      else:
        # the user already exists
        # TO DO
        pass
    elif login_form.is_valid():
      print "logging in.."
      if user_profile_exists(login_form.cleaned_data['email']):
        print "login user exists"
        login_user(login_form.cleaned_data['email'], request)
        return HttpResponseRedirect(reverse('event', args=[event_id]))
      else:
        # Do Nothing (page will reload with no one logged in)
        pass
    elif logout_form.is_valid():
      logout_user(request)

    print "aoeu"
    if recommend_form.is_valid() and user_is_logged_in(request):
      subject = "You have recieved a link"
      message_template = loader.get_template('events/recommend.txt')
      message_context = Context({
        'event': event,
        'from': request.session['login_email'],
      })
      message = message_template.render(message_context)
      email = EmailMessage(
        subject,
        message,
        request.session['login_email'],
        [recommend_form.cleaned_data['to_list']],
      )

      #email = EmailMessage('hello', 'some boddyy', 'aoeulover@gmail.com',
      #['dionyses@gmail.com'])
      email.send()

    elif register_event_form.is_valid():
      print "reg form valid"
      if user_is_logged_in(request):
        print "user logged in"
        register_user_for_event(request)      


  if user_is_logged_in(request):
    if request.session['user_registered'] is None and is_first_redirect(request):
      request.session['first_redirect'] = "False"
      request.session['was_redirected'] = "True"
      return HttpResponseRedirect(reverse('register', args=[event_id]))
 
  context_data = {
    'event': event,
    'state': state,
    'stateOffsets': event.state_offsets,
    'login_form': LoginForm(),
    'logout_form': LogoutForm(),
    'register_event_form': RegisterEventForm(),
    'user_profile_form': UserProfileForm(),
    'recommend_form': RecommendForm(),
  }

  return render_to_response(template, context_data, context_instance = RequestContext(request))

def is_first_redirect(request):
  return request.session['first_redirect'] is None or request.session['first_redirect'] == "True"

def user_profile_exists(email):
  user = UserProfile.objects.filter(email=email)

  if len(user) >= 1:
    return True

  return False

def login_user(email, request):
  request.session['login_email'] = email

def user_is_logged_in(request):
  print request.session['login_email']
  return not request.session['login_email'] is None

def logout_user(request):
  request.session['login_email'] = None

def register_user_for_event(request):
  registration = Registration.objects.filter(email=request.session['login_email']).filter(event=request.session['event_id'])

  print len(registration)
  if len(registration) == 0:
    registration = Registration()
    registration.email = request.session['login_email']
    registration.event = Event.objects.get(id=request.session['event_id'])
    #registration.ip = # TO DO
    registration.save()
    print "saved"

  request.session['user_registered'] = "True"

def presentation(request, event_id, state = None):
  event = Event.objects.get(id = event_id)
  if state == None:
    state = event.state

  template = 'events/presentation_%s.html' % state
  
  return render_to_response([template, 'events/presentation.html'], {'event': event, 'state': state}, context_instance = RequestContext(request))
