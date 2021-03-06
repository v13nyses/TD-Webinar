from django.db import models

# Create your models here.
class UserProfile(models.Model):
  email = models.EmailField()
  title = models.ForeignKey('Title', blank=True, null=True)
  first_name = models.CharField(max_length=200, blank=True)
  last_name = models.CharField(max_length=200, blank=True)
  city = models.CharField(max_length=200, blank=True)
  province = models.CharField(max_length=200, blank=True)
  postal_code = models.CharField(max_length=6, blank=True)
  upcoming_events = models.BooleanField()
  refer_type = models.ForeignKey('ReferType')
  ip_address = models.IPAddressField(blank=True)

class Title(models.Model):
  name = models.CharField(max_length=10)

  def __unicode__(self):
    return self.name

class ReferType(models.Model):
  name = models.CharField(max_length=200)
  text = models.CharField(max_length=200, blank=True)

  def __unicode__(self):
    return self.name
