from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context

from registration.models import Registration
from userprofiles.models import UserProfile
from events.models import Event

from events.forms import LoginForm, LogoutForm
from userprofiles.forms import UserProfileForm
from registration.forms import RegisterEventForm

from events.views import get_user_profile_registration, get_event, user_is_logged_in

def register(request, event_id = None):
  profile = None
  registration = None
  request.session['user_registered'] = None
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

  login_form = LoginForm()
  logout_form = LogoutForm()
  register_event_form = RegisterEventForm()
  user_profile_form = UserProfileForm()

  if request.method == "POST":
    login_form = LoginForm(request.POST)
    logout_form = LogoutForm(request.POST)
    register_event_form = RegisterEventForm(request.POST)
    user_profile_form = UserProfileForm(request.POST)

    if user_profile_form.is_valid():
      if not user_profile_exists(user_profile_form.cleaned_data['email']):
        usr = user_profile_form.save(commit=False)
        usr.ip_address = request.META['REMOTE_ADDR']
        usr.save()
        login_user(request, user_profile_form.cleaned_data['email'])
        register_user_for_event(request, event, usr)
        return HttpResponseRedirect(reverse('event', args=[event_id]))
      else:
        # the user already exists
        # TO DO
        user_profile_form = UserProfileForm()
        pass
    elif login_form.is_valid():
      if user_profile_exists(login_form.cleaned_data['email']):
        login_user(request, login_form.cleaned_data['email'])
        #if is_first_redirect(request):
        #  return HttpResponseRedirect(reverse('register', args=[event_id, settings.REGISTRATION_MESSAGE]))
        #else:
        return HttpResponseRedirect(reverse('event', args=[event_id]))
      else:
        # Do Nothing (page will reload with no one logged in)
        logout_form = LogoutForm()
        pass
    elif logout_form.is_valid():
      logout_user(request)
      login_form = LoginForm()
      user_profile_form = UserProfileForm()
      register_event_form = RegisterEventForm()
    
    if user_is_logged_in(request):
      if register_event_form.is_valid():
        register_user_for_event(request, event, profile)
        return HttpResponseRedirect(reverse('event', args=[event_id]))

  context_data = {
    'event': event,
    'login_form': login_form,
    'logout_form': logout_form,
    'register_event_form': register_event_form,
    'user_profile_form': user_profile_form,
  }

  return render_to_response('register.html', context_data, context_instance = RequestContext(request))


def register_user_for_event(request, event, profile):
  registration = Registration.objects.filter(user_profile=profile, event=event.id)

  if len(registration) == 0:
    registration = Registration()
    registration.user_profile = profile
    registration.event = event
    registration.ip_address = request.META['REMOTE_ADDR']
    registration.save()

  request.session['user_registered'] = "True"

def login_user(request, email):
  request.session['login_email'] = email

def user_profile_exists(user_email):
  if user_email:
    user = UserProfile.objects.filter(email = user_email)

    if len(user) == 1:
      return True

  return False

def logout_user(request):
  request.session['login_email'] = None
  request.session['use_registered'] = None
