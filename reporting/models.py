from django.db import models

# Create your models here.
class Engagement(models.Model):
  email = models.ForeignKey('userprofiles.UserProfile')
  event = models.ForeignKey('events.Event')
  ip_address = models.IPAddressField()
  #location = models.ForeignKey('geoip.City')
  
