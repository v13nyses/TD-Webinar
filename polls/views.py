from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from polls.models import Poll, Choice

# Create your views here.
def vote(request, poll_id):
  poll = get_object_or_404(Poll, pk=poll_id)
  try:
    selected_choice = poll.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    return render_to_response('polls/slide_poll.html', {
      'poll': poll,
      'error_message': 'You didn''t select a choice.',
#    })
    }, context_instance=RequestContext(request))
  else:
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect('presentations/slide.html')
