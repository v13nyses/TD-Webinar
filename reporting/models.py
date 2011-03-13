from django.db import models

# Create your models here.
class Engagement(models.Model):
  profile = models.ForeignKey('userprofiles.UserProfile')
  event = models.ForeignKey('events.Event')
  ip_address = models.IPAddressField(blank = True, null = True)
#  start_time = models.IntegerField()
#  duration = models.IntegerField()
  #location = models.ForeignKey('geoip.City')

class Block(models.Model):
  engagement = models.ForeignKey('Engagement')
  start = models.DateTimeField()
  seconds = models.IntegerField(blank=True,null=True)  
