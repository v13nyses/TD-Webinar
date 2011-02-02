import os
from django.conf import settings
from events.models import Event
from presentations.models import Presentation, PresenterType, Presenter
from django.core.files.uploadedfile import InMemoryUploadedFile
from forms import PresentationForm, EventForm

class FormController():

  def __init__(self, request, FormClass, instance = None):
    if request.POST:
      self.form = FormClass(request.POST, request.FILES, instance = instance)
    else:
      self.form = FormClass(instance = instance)

  def save():
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
      if field_name == 'lobby_video_string' and field_value != '':
        video_id, player_id = field_value.split('-')
        video = Video()
        video.video_id = video_id
        video.player_id = player_id
        video.save()
        event.lobby_video = video
      elif type(field_value) == InMemoryUploadedFile:
        filepath = event_upload_to(event, uploaded_file.name)
        self.upload_file(field_value, upload_to = os.path.dirname(upload_to))
        event.__dict__[field_name] = filepath
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
