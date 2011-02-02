from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from events.models import Event
from datetime import datetime
from pytz import timezone

from events.forms import LoginForm, LogoutForm
from userprofiles.forms import UserProfileForm

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
def event(request, event_id = None):
  if not request.session.has_key('login_email'):
    request.session['login_email'] = None

  if request.method == "POST":
    login_form = LoginForm(request.POST)
    logout_form = LogoutForm(request.POST)    

    if logout_form.is_valid():
      if logout_form.cleaned_data['logout'] == "true":
        request.session['login_email'] = None
    elif login_form.is_valid():
      request.session['login_email'] = login_form.cleaned_data['email']

  login_form = LoginForm()
  logout_form = LogoutForm()
  user_profile_form = UserProfileForm()

  # if we didn't get an event id, grab the newest event
  if event_id == None:
    try:
      event = Event.objects.order_by('-live_start_date')[0]
    except IndexError:
      # create a blank event if there aren't any yet
      event = Event()

  else:
    event = Event.objects.get_or_create(id = event_id)

  return render_to_response('event.html', {
                              'event': event,
                              'login_form': login_form, 
                              'logout_form': logout_form,
                              'user_profile_form': user_profile_form,
                            }, 
                            context_instance = RequestContext(request))
