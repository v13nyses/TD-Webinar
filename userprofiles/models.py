from django.db import models

# Create your models here.
class UserProfile(models.Model):
  email = models.EmailField()
  title = models.ForeignKey('Title')
  first_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  city = models.CharField(max_length=200)
  province = models.CharField(max_length=200)
  postal_code = models.CharField(max_length=6)
  upcoming_events = models.BooleanField()
  refer_type = models.ForeignKey('ReferType')

class Title(models.Model):
  name = models.CharField(max_length=10)

  def __unicode__(self):
    return self.name

class ReferType(models.Model):
  name = models.CharField(max_length=200)
  text = models.CharField(max_length=200, blank=True)

  def __unicode__(self):
    return self.name
