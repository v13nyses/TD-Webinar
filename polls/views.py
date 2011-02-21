from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from polls.models import Poll, Choice, Vote
from userprofiles.models import UserProfile
from events.views import user_is_logged_in

# Create your views here.
def vote(request, poll_id):
  poll = get_object_or_404(Poll, pk=poll_id)
  try:
    selected_choice = poll.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    return render_to_response('polls/slide_poll.html', {
      'poll': poll,
    }, context_instance=RequestContext(request))
  else:
    vote = Vote()
    vote.choice = selected_choice

    if user_is_logged_in(request):
      profile = UserProfile.objects.get(email = request.session['login_email'])
      vote.user_profile = profile
    vote.save()

    return render_to_response('presentations/slide.html', {'slide': poll},
      context_instance=RequestContext(request))
    #return HttpResponseRedirect('presentations/slide.html')
