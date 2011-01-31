from registration.forms import RegisterForm, LoginForm

# Create your views here.
def register(request, event_id = None):
  if request.method == "POST":
    form = RegisterForm(request.POST)

    if form.is_valid():
      if not is_registered_for_event(request, form.email, event_id):
        register_for_event(request, form.email, event_id)
      
      login_for_event(request, form.email, event_id)

      return HttpResponseRedirect('registration/login.html')
    else:
      form.invalid = True
  else:
    form = RegisterForm()
  
  return render_to_response('registration/register.html', {'form': form})

def user_has_session(request):
  return not request.session['loggin_email'] is None

def is_registered_for_event(request, email = None, event_id = None):
  if email and event_id:
      registrations = Registration.objects.filter(email=email).filter(
        event=Event.objects.get(id=event_id)
      )

      if len(registrations) > 0:
        return True

  return False

def register_for_event(request, email = None, event_id = None):
  r = Registration()
  r.email = form.email
  r.event = Event.objects.get(id=event_id)
  r.save()
