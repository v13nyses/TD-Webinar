from django.db import models

from events.models import Event

# Create your models here.
class Registration(models.Model):
  email = models.CharField(max_length=200)
  event = models.ForeignKey('events.Event')
  ip = models.CharField(max_length=200)
