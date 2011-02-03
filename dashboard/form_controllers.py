import os
from django.conf import settings
from events.models import Event, event_upload_base_path
from presentations.models import Presentation, PresenterType, Presenter, Video
from django.core.files.uploadedfile import InMemoryUploadedFile
from forms import PresentationForm, EventForm

class FormController():

  def __init__(self, request, FormClass, instance = None):
    if request.POST:
      self.form = FormClass(request.POST, request.FILES, instance = instance)
    else:
      self.form = FormClass(instance = instance)

  def delete(self):
    self.form.instance.delete()

  def save(self):
    pass

  def upload_file(self, uploaded_file, upload_to = ''):
    filepath = os.path.join(settings.MEDIA_ROOT, upload_to, uploaded_file.name)

    try:
      destination = open(filepath, 'wb+')
    except IOError:
      os.mkdir(os.path.dirname(filepath))
      destination = open(filepath, 'wb+')

    for chunk in uploaded_file.chunks():
      destination.write(chunk)
    destination.close()

    return os.path.join(upload_to, uploaded_file.name)

class EventFormController(FormController):
  def __init__(self, request, instance = None):
    FormController.__init__(self, request, EventForm, instance)

  def save(self):
    if not self.form.is_valid():
      return False

    data = self.form.cleaned_data
    event = self.form.instance

    for field_name in data:
      field_value = data[field_name]
      # figure out a better way to do this... __dict__ stores 'lobby_video_id'
      if field_name == 'lobby_video':
        event.lobby_video = field_value
      elif type(field_value) == InMemoryUploadedFile:
        base_path = event_upload_base_path(event)
        event.__dict__[field_name] = self.upload_file(field_value, upload_to = base_path)
      else:
        event.__dict__[field_name] = field_value
    
    if event.presentation_id == None:
      presentation = Presentation()
      presentation.save()
      event.presentation = presentation

    event.save()

    return True

class PresentationFormController(FormController):
  def __init__(self, request, instance = None):
    FormController.__init__(self, request, PresentationForm, instance)

  def save(self, event):
    if not self.form.is_valid():
      return False

    data = self.form.cleaned_data

    presenter = self.form.instance
    presenter.name = data['name']
    presenter.description = data['description']
    presenter.job_title = data['job_title']
    presenter.presenter_type = PresenterType.objects.get(id = data['presenter_type'])
    if data['photo']:
      presenter.photo = self.upload_file(data['photo'], upload_to = 'presenters')
    presenter.save()

    presentation = event.presentation
    presentation.presenters.add(presenter)
    presentation.save()

    return True
