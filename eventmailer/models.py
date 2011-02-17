from django.db import models
from django.conf import settings
from greatape import MailChimp, MailChimpError
from userprofiles.models import UserProfile
from registration.models import Registration
from events.models import Event
from datetime import timedelta
from pytz import timezone
import logging

logger = logging.getLogger(__name__)

class MailChimpEvent(models.Model):
  list_segment_id = models.CharField(max_length = 30)
  campaign_24_hour_id = models.CharField(max_length = 30)
  campaign_1_hour_id = models.CharField(max_length = 30)

  event = models.OneToOneField('events.Event')

  def create_segment(self):
    mailchimp = MailChimp(settings.MAILCHIMP_API_KEY)
    try:
      self.list_segment_id = mailchimp.listAddStaticSegment(
          id = settings.MAILCHIMP_LIST_ID,
          name = self.event.name
      )
    except MailChimpError as error:
      logger.error("MailChimp segment already exists: %s" % error.msg)
      # find the matching segment
      logger.info("Finding segments with name: %s" % self.event.name)
      for segment in mailchimp.listStaticSegments(id = settings.MAILCHIMP_LIST_ID):
        if segment['name'] == self.event.name:
          self.list_segment_id = segment['id']
          logger.info("Found matching segment for '%s': %s" % (self.event.name, segment['id']))

  def create_campaign(self, subject_format, time_str, schedule_time = None):
    mailchimp = MailChimp(settings.MAILCHIMP_API_KEY)
    campaign_id = mailchimp.campaignCreate(
        type = 'regular',
        content = {'html': self.event.description},
        segment_opts = {'match': 'all', 'conditions': [{
                              'field': 'static_segment',
                              'op': 'eq',
                              'value': self.list_segment_id
                        }]},
        options = {
          'list_id': settings.MAILCHIMP_LIST_ID,
          'subject': subject_format.format(event = self.event.name, time = time_str), 
          'from_email': settings.MAILCHIMP_FROM_EMAIL,
          'from_name': settings.MAILCHIMP_FROM_NAME,
          'to_email': settings.MAILCHIMP_TO_EMAIL,
        }
    )

    if schedule_time != None:
      try:
        mailchimp.campaignSchedule(cid = campaign_id, schedule_time = schedule_time)
      except MailChimpError as error:
        logger.error("Campaign scheduled in the past: %s" % error.msg)

    return campaign_id

  def gmt_timestamp(self, datetime):
    return datetime.astimezone(timezone('GMT')).replace(tzinfo = None).isoformat(sep = " ")

  def create_campaigns(self):
    time_24_hours = self.gmt_timestamp(self.event.live_offset(timedelta(hours = -24)))
    time_1_hour = self.gmt_timestamp(self.event.live_offset(timedelta(hours = -1)))

    logger.info("Creating MailChimp Campaigns:")
    logger.info(" - 24 Hour Reminder (%s)" % time_24_hours)
    logger.info(" - 1 Hour reminder (%s)" % time_1_hour)

    self.create_segment()
    self.create_campaign(settings.MAILCHIMP_SUBJECTS['reminder'], '24 hours', time_24_hours)
    self.create_campaign(settings.MAILCHIMP_SUBJECTS['reminder'], '1 hour', time_1_hour)

def mailchimp_template_choices():
  mailchimp = MailChimp(settings.MAILCHIMP_API_KEY)
  templates = mailchimp.campaignTemplates()

  choices = []
  for template in templates:
    choices.append((template['id'], template['name']))

  return choices

def setup_event(sender, instance = None, created = False, **kwargs):
  if created:
    event_mailer = MailChimpEvent()
    event_mailer.event = instance
    event_mailer.create_campaigns()
    event_mailer.save()

def register_user(sender, instance = None, created = False, **kwargs):
  logger.info("Registering user: %s, created: %s" % (instance.email, created))
  if created:
    # lookup the profile for the registered user
    profile = UserProfile.objects.get(email = instance.email)
    mailchimp_event = MailChimpEvent.objects.get(event = instance.event)
    mailchimp = MailChimp(settings.MAILCHIMP_API_KEY)
    result = mailchimp.listSubscribe(
        id = settings.MAILCHIMP_LIST_ID, 
        email_address = instance.email,
        merge_vars = {
          'FNAME': profile.first_name,
          'LNAME': profile.last_name,
          'ADDRESS': {
            'city': profile.city,
            'state': profile.province,
            'zip': profile.postal_code,
            'country': 'Canada'
          },
          'EVENT_NAME': instance.event.name,
        },
        double_optin = False,
        welcome_email = True,
        update_existing = True
    )
    logger.info("Adding %s to list '%s', result: %s" % (instance.email, settings.MAILCHIMP_LIST_ID, result))
    result = mailchimp.listStaticSegmentAddMembers(
        id = settings.MAILCHIMP_LIST_ID,
        seg_id = mailchimp_event.list_segment_id,
        batch = [instance.email]
    )
    logger.info("Adding %s to list segment '%s': %s" % (instance.email, mailchimp_event.list_segment_id, result))
                            


models.signals.post_save.connect(setup_event, sender = Event)
models.signals.post_save.connect(register_user, sender = Registration)
