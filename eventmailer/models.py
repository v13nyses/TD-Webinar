from django.db import models
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
from greatape import MailChimp, MailChimpError
from userprofiles.models import UserProfile
from registration.models import Registration
from events.models import Event
from datetime import timedelta, datetime
from pytz import timezone
import logging

logger = logging.getLogger(__name__)

class MailChimpEvent(models.Model):
  list_segment_id = models.CharField(max_length = 30)
  participated_segment_id = models.CharField(max_length = 30)
  campaign_24_hour_id = models.CharField(max_length = 30)
  campaign_1_hour_id = models.CharField(max_length = 30)
  campaign_sorry_id = models.CharField(max_length = 30)
  campaign_thanks_id = models.CharField(max_length = 30)

  event = models.OneToOneField('events.Event')

  def create_segment(self, name):
    segment_name = name[:25]
    mailchimp = MailChimp(settings.MAILCHIMP_API_KEY)
    try:
      segment_id = mailchimp.listAddStaticSegment(
          id = settings.MAILCHIMP_LIST_ID,
          name = segment_name
      )
    except MailChimpError as error:
      logger.error("MailChimp segment already exists: %s" % error.msg)
      # find the matching segment
      logger.info("Finding segments with name: %s" % segment_name)
      for segment in mailchimp.listStaticSegments(id = settings.MAILCHIMP_LIST_ID):
        if segment['name'] == segment_name:
          segment_id = segment['id']
          logger.info("Found matching segment for '%s': %s" % (segment_name, segment['id']))
    
    return segment_id

  def create_campaign(self, subject_format, schedule_time = None, time_str = None, template_id = None):
    mailchimp = MailChimp(settings.MAILCHIMP_API_KEY)
    campaign_id = mailchimp.campaignCreate(
        type = 'regular',
        content = {'html_mid_content00': self.event.description},
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
          'template_id': template_id,
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

  def create_event_finished_campaigns(self):
    finished_date = self.event.live_stop_date.replace(tzinfo = timezone(settings.TIME_ZONE))
    event_finished_time = self.gmt_timestamp(finished_date)

    mailchimp = MailChimp(settings.MAILCHIMP_API_KEY)
    self.campaign_sorry_id = mailchimp.campaignCreate(
        type = 'regular',
        content = {'html_mid_content00': self.event.description},
        segment_opts = {'match': 'all', 'conditions': [{
                              'field': 'static_segment',
                              'op': 'eq',
                              'value': self.participated_segment_id
                        }]},
        options = {
          'list_id': settings.MAILCHIMP_LIST_ID,
          'subject': settings.MAILCHIMP_SUBJECTS['finished_sorry_we_missed'],
          'from_email': settings.MAILCHIMP_FROM_EMAIL,
          'from_name': settings.MAILCHIMP_FROM_NAME,
          'to_email': settings.MAILCHIMP_TO_EMAIL,
          'template_id': self.event.template_missed_you,
        }
    )

    self.campaign_thanks_id = mailchimp.campaignCreate(
        type = 'regular',
        content = {'html_mid_content00': self.event.description},
        segment_opts = {'match': 'all', 'conditions': [
                            {
                              'field': 'static_segment',
                              'op': 'ne',
                              'value': self.participated_segment_id
                            },
                            {
                              'field': 'static_segment',
                              'op': 'eq',
                              'value': self.list_segment_id
                            }]},
        options = {
          'list_id': settings.MAILCHIMP_LIST_ID,
          'subject': settings.MAILCHIMP_SUBJECTS['finished_thank_you'],
          'from_email': settings.MAILCHIMP_FROM_EMAIL,
          'from_name': settings.MAILCHIMP_FROM_NAME,
          'to_email': settings.MAILCHIMP_TO_EMAIL,
          'template_id': self.event.template_thank_you,
        }
    )
    try:
      mailchimp.campaignSchedule(cid = self.campaign_thanks_id, schedule_time = event_finished_time)
      mailchimp.campaignSchedule(cid = self.campaign_sorry_id, schedule_time = event_finished_time)
    except MailChimpError as error:
      logger.error("Campaign scheduled in the past: %s" % error.msg)

  def create_campaigns(self):
    time_24_hours = self.gmt_timestamp(self.event.live_offset(timedelta(hours = -24)))
    time_1_hour = self.gmt_timestamp(self.event.live_offset(timedelta(hours = -1)))

    logger.info("Creating MailChimp Campaigns:")
    logger.info(" - 24 Hour Reminder (%s)" % time_24_hours)
    logger.info(" - 1 Hour reminder (%s)" % time_1_hour)

    self.list_segment_id = self.create_segment(self.event.slug)
    self.participated_segment_id = self.create_segment("attended: %s" % self.event.slug)
    self.create_campaign(settings.MAILCHIMP_SUBJECTS['reminder'], 
                         time_24_hours, '24 hours', self.event.template_24_hour)
    self.create_campaign(settings.MAILCHIMP_SUBJECTS['reminder'], 
                         time_1_hour, '1 hours', self.event.template_1_hour)
    self.create_event_finished_campaigns()

def mailchimp_template_choices():
  mailchimp = MailChimp(settings.MAILCHIMP_API_KEY)
  templates = mailchimp.campaignTemplates()

  choices = []
  for template in templates:
    choices.append((template['id'], template['name']))

  return choices

def setup_event(sender, instance = None, created = False, **kwargs):
  if created and instance.live_start_date > datetime.now():
    event_mailer = MailChimpEvent()
    event_mailer.event = instance
    event_mailer.create_campaigns()
    event_mailer.save()

def register_user(sender, instance = None, created = False, **kwargs):
  logger.info("Registering user: %s, created: %s" % (instance.user_profile.email, created))
  if created:
    send_welcome_email(instance)
    # lookup the profile for the registered user
    profile = instance.user_profile
    try:
      mailchimp_event = MailChimpEvent.objects.get(event = instance.event)
      mailchimp = MailChimp(settings.MAILCHIMP_API_KEY)
      event = instance.event
      event_start_datetime = event.start_date_timezone('America/Toronto').strftime('%A, %b %d, %I:%M %p')
      event_start_date = event.start_date_timezone('America/Toronto').strftime('%A, %b %d')
      event_start_time = event.start_date_timezone('America/Toronto').strftime('%I:%M %p')
      result = mailchimp.listSubscribe(
          id = settings.MAILCHIMP_LIST_ID, 
          email_address = profile.email,
          merge_vars = {
            'FNAME': profile.first_name,
            'LNAME': profile.last_name,
            'ADDRESS': {
              'city': profile.city,
              'state': profile.province,
              'zip': profile.postal_code,
              'country': 'Canada'
            },
            'EVENT_TITLE': instance.event.name,
            'EVENT_DATETIME': event_start_datetime,
            'EVENT_DATE': event_start_date,
            'EVENT_TIME': event_start_time,
            'EVENT_TAGLINE': event.short_description,
            'EVENT_LONGDESC': event.description,
            'EVENT_OUTLOOKLINK': "http://home.v13inc.com/%s/%s" % (settings.MEDIA_URL, event.outlook_file)
          },
          double_optin = False,
          welcome_email = True,
          update_existing = True
      )
      logger.info("Adding %s to list '%s', result: %s" % (profile.email, settings.MAILCHIMP_LIST_ID, result))
      result = mailchimp.listStaticSegmentAddMembers(
          id = settings.MAILCHIMP_LIST_ID,
          seg_id = mailchimp_event.list_segment_id,
          batch = [profile.email]
      )
      logger.info("Adding %s to list segment '%s': %s" % (profile.email, mailchimp_event.list_segment_id, result))
    except MailChimpEvent.DoesNotExist:
      logger.info("Unable to add user to list, no MailChimpEvent for current event")
                            
def view_event_live(event, profile):
    mailchimp_event = MailChimpEvent.objects.get(event = event)
    mailchimp = MailChimp(settings.MAILCHIMP_API_KEY)
    result = mailchimp.listStaticSegmentAddMembers(
        id = settings.MAILCHIMP_LIST_ID,
        seg_id = mailchimp_event.participated_segment_id,
        batch = [profile.email]
    )
    logger.info("Adding %s to 'thank you' segment '%s': %s" % (profile.email, mailchimp_event.list_segment_id, result))

def send_welcome_email(registration):
  profile = registration.user_profile
  context = {
    'event': registration.event,
    'registration': registration,
    'profile': profile,
    'settings': settings
  }
  html_message = render_to_string('events/welcome_email.html', context)
  message = ''
  email = EmailMultiAlternatives(
    settings.WELCOME_EMAIL_SUBJECT.format(
      first_name = profile.first_name, 
      last_name = profile.last_name,
      event = registration.event.name),
    message,
    settings.MAILCHIMP_FROM_EMAIL,
    [profile.email]
  )
  email.attach_alternative(html_message, "text/html")
  email.send()
  logger.info("sending welcome email to: %s" % profile.email)

models.signals.post_save.connect(setup_event, sender = Event)
models.signals.post_save.connect(register_user, sender = Registration)
