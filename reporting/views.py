from django.http import HttpResponse
from events.models import Event
from userprofiles.models import UserProfile
from models import Engagement
import logging
import ipdb
import simplejson as json

logger = logging.getLogger(__name__)

def update_engagement(request, event_id, start_time, duration):
  event = Event.objects.get(id = event_id)
  if request.session.has_key('login_email'):
    profile = UserProfile.objects.get(email = request.session['login_email'])

    engagement_objects = Engagement.objects.filter(profile = profile, event = event)
    if len(engagement_objects) > 0:
      engagement_data = engagement_objects[0]
    else:
      engagement_data = Engagement()
      engagement_data.event = event
      engagement_data.profile = profile

    engagement_data.start_time = start_time
    engagement_data.duration = duration

    engagement_data.save()

    result = {
      'success': True,
    }
    logger.info('Updating engagement date for "%s", duration: %s' % (profile.email, duration))
  else:
    result = {
      'success': False,
      'error': 'User not logged in'
    }

  return HttpResponse(json.dumps({'result': result}), mimetype = 'application/javascript')
