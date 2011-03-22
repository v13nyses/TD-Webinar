from django.http import HttpResponse
import logging
import ipdb
import simplejson as json

from events.models import Event
from userprofiles.models import UserProfile
from reporting.models import Engagement, Block

logger = logging.getLogger(__name__)

def update_engagement(request, event_id, start_offset, duration):
  event = Event.objects.get(id = event_id)

  if request.session.has_key('login_email'):
    profile = UserProfile.objects.filter(email = request.session['login_email'])

    if len(profile) == 1:
      profile = profile[0]
      engagement_objects = Engagement.objects.filter(profile = profile, event = event)

      if len(engagement_objects) == 0:
        engagement_data = Engagement()
        engagement_data.event = event
        engagement_data.profile = profile
        engagement_data.save()

        block = Block()
        block.engagement = engagement_data
        block.start_offset = start_offset
        block.seconds = duration
        block.save()
      else:
        engagement_data = engagement_objects[0]
        blocks = Block.objects.filter(engagement = engagement_data, start_offset = start_offset)

        if len(blocks) == 0:
          block = Block()
          block.engagement = engagement_data
          block.start_offset = start_offset
          block.seconds = int(duration)
          block.save()
        else:
          block = blocks[0]
          block.seconds = block.seconds + int(duration)    
          block.save()

      result = {
        'success': True,
      }
      logger.info('Updating engagement date for "%s", duration: %s' % (profile.email, duration))
    else:
      result = {
        'success': False,
        'error': 'User does not exist'
      }
  else:
    result = {
      'success': False,
      'error': 'User not logged in'
    }

  return HttpResponse(json.dumps({'result': result}), mimetype = 'application/javascript')
