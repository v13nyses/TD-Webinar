from django.db import models

# Create your models here.
class Engagement(models.Model):
  email = models.ForeignKey('userprofiles.UserProfile')
  event = models.ForeignKey('events.Event')
  ip = models.IPAddressField()
  location = models.ForeignKey('geoip.City')
  
