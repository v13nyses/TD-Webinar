from django.db import models

from events.models import Event

# Create your models here.
class Registration(model.models):
  email = ...
  event = models.ForeignKey("Event")
