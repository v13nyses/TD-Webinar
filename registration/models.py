from django.db import models

from events.models import Event
from userprofiles.models import UserProfile

# Create your models here.
class Registration(models.Model):
  user_profile = models.ForeignKey('userprofiles.UserProfile')
  event = models.ForeignKey('events.Event')
  viewed_live = models.BooleanField(default = False)
  ip_address = models.IPAddressField()
  completed_exit_survey = models.CharField(max_length=200,default="False")
