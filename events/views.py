from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from events.models import Event
from datetime import datetime
from pytz import timezone

from events.forms import LoginForm, LogoutForm
from userprofiles.forms import UserProfileForm
from registration.forms import RegisterEventForm

from registration.models import Registration
from userprofiles.models import UserProfile

# used by urls:
#   event/<event_id>/slides/
def slides(request):
  # TO DO
  pass

# used by urls:
#   event/<event_id>/slide/<slide_id>/
def slide(request, slide_id = None):
  # TO DO
  pass

# used by urls:
#   event/
#   event/<event_id>/
def event(request, event_id = None, state = None):
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

  if state == None:
    state = event.state

  request.session['event_id'] = event.id

  if not request.session.has_key('login_email'):
    request.session['login_email'] = None
  else:
    reg = Registration.objects.filter(email=request.session['login_email']).filter(event=event.id)

    if len(reg) == 0:
      request.session['user_registered'] = None
    else:
      request.session['user_registered'] = "True"

  if request.method == "POST":
    login_form = LoginForm(request.POST)
    logout_form = LogoutForm(request.POST)
    register_event_form = RegisterEventForm(request.POST)
    user_profile_form = UserProfileForm(request.POST)

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
      if user_profile_exists(login_form.cleaned_data['email']):
        login_user(login_form.cleaned_data['email'], request)
      else:
        # Do Nothing (page will reload with no one logged in)
        pass
    elif logout_form.is_valid():
      logout_user(request)

    if register_event_form.is_valid():
      if user_is_logged_in(request):
        register_user_for_event(request)      
  
  context_data = {
    'event': event,
    'state': state,
    'stateOffsets': event.state_offsets,
    'login_form': LoginForm(),
    'logout_form': LogoutForm(),
    'register_event_form': RegisterEventForm(),
    'user_profile_form': UserProfileForm(),
  }

  return render_to_response('event.html', context_data, context_instance = RequestContext(request))

def user_profile_exists(email):
  user = UserProfile.objects.filter(email=email)

  if len(user) >= 1:
    return True

  return False

def login_user(email, request):
  request.session['login_email'] = email

def user_is_logged_in(request):
  return not request.session['login_email'] is None

def logout_user(request):
  request.session['login_email'] = None

def register_user_for_event(request):
  registration = Registration.objects.filter(email=request.session['login_email']).filter(event=request.session['event_id'])

  if len(registration) == 0:
    registration = Registration()
    registration.email = request.session['login_email']
    registration.event = Event.objects.get(id=request.session['event_id'])
    #registration.ip = # TO DO
    registration.save()

  request.session['user_registered'] = "True"

def presentation(request, event_id, state = None):
  event = Event.objects.get(id = event_id)
  if state == None:
    state = event.state

  template = 'events/presentation_%s.html' % state
  
  return render_to_response([template, 'events/presentation.html'], {'event': event, 'state': state}, context_instance = RequestContext(request))
