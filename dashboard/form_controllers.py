import os, ipdb
from django.conf import settings
from events.models import Event, event_upload_base_path
from presentations.models import Presentation, PresenterType, Presenter, Video, slide_upload_to
from django.core.files.uploadedfile import InMemoryUploadedFile
from forms import PresentationForm, EventForm, SlideForm

class FormController():

  def __init__(self, request, FormClass, instance = None, initial = None):
    self.request = request

    if request.POST:
      self.form = FormClass(request.POST, request.FILES, instance = instance, initial = initial)
    else:
      self.form = FormClass(instance = instance, initial = initial)

  def delete(self):
    self.form.instance.delete()

  def save(self):
    pass
  
  def set_fieldset_label(self, label, fieldset_num = 0):
    # TODO: Figure out a better way to change fieldset labels.
    # Tuples aren't mutable, so we need to recreate the fieldsets with
    # a new label
    fieldsets = self.form.fieldsets.fieldsets
    new_fieldset = (label, fieldsets[fieldset_num][1])
    fieldsets[fieldset_num] = new_fieldset

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

  def set_action(self, action, presenter = None):
    if action == 'add':
      label = "Add a Presenter"
    elif action == 'edit':
      label = presenter.name
    else:
      label = self.form.Meta.fieldsets[0][0]

    self.set_fieldset_label(label)

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

class SlideFormController(FormController):
  def __init__(self, request, event, instance = None):
    self.event = event
    video_id = self.event.presentation.video.id
    FormController.__init__(self, request, SlideForm, instance, initial = {'video': video_id})

  def set_action(self, action):
    if action == 'add':
      label = 'Add a Slide'
    elif action == 'edit':
      label = 'Edit Slide'
    else:
      label = self.form.Meta.fieldsets[1][0]

    self.set_fieldset_label(label, 1)

  def save(self):
    if not self.form.is_valid():
      return False

    data = self.form.cleaned_data
    slide_set = self.event.presentation.slide_set

    slide = self.form.instance
    slide.slide_set = slide_set
    slide.offset = data['offset']
    if data['image']:
      base_path = os.path.dirname(slide_upload_to(slide, data['image'].name))
      slide.image = self.upload_file(data['image'], upload_to = base_path)

    self.event.presentation.video = data['video']
    slide.save()
    self.event.presentation.save()

    return True
