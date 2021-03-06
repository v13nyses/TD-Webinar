import os, ipdb
from django.conf import settings
from events.models import Event, event_upload_base_path
from presentations.models import Presentation, PresenterType, Presenter, Video, Slide, SlideSet, slide_upload_to
from polls.models import Poll, Choice
from django.core.files.uploadedfile import InMemoryUploadedFile
from forms import PresentationForm, EventForm, SlideForm
import datetime
import ipdb
import utils

class FormController():

  def __init__(self, request, FormClass = None, instance = None, initial = None):
    self.request = request
    
    if FormClass:
      if request.POST:
        self.form = FormClass(request.POST, request.FILES, instance = instance, initial = initial)
      else:
        self.form = FormClass(instance = instance, initial = initial)

  def delete(self):
    self.form.instance.delete()

  def save(self):
    pass

  def submit(self, continue_path = None, back_path = None):
    if not self.request.POST:
      return False

    save_result = True
    submit_button = self.request.POST['submit'].lower()
    print '!!! %s' % submit_button
    if submit_button.find('save') != -1:
      save_result = self.save()

    if submit_button.find('back') != -1 and save_result and back_path:
      return back_path

    if submit_button.find('continue') != -1 and save_result:
      return continue_path 

    return False

  
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

    # remove the slides field, since its not part of the event model
    slides_value = data.pop('slides')
    timing_value = data.pop('timing')

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

    # save the event now to generate an id
    event.save()

    if event.presentation.slide_set == None:
      slide_set = SlideSet()
      slide_set.presentation = event.presentation
      slide_set.save()
      event.presentation.slide_set = slide_set
      event.presentation.save()

    base_path = event_upload_base_path(event)
    # convert the slides pdf into images
    if slides_value:
      slides_path = self.upload_file(slides_value, upload_to = base_path)
      image_path = slide_upload_to(event, 'slide.png')

      # create the slides/ directory
      dir_path = os.path.join(settings.MEDIA_ROOT, base_path, 'slides')
      if not os.path.exists(dir_path):
        os.mkdir(dir_path)

      utils.pdf_to_images(slides_path, image_path)

      # loop through all the images
      image_format = slide_upload_to(event, 'slide-%s.png')
      image = image_format % 0

      i = 0
      slides_test = []
      while os.path.exists(os.path.join(settings.MEDIA_ROOT, image)):
        slide = Slide()
        slide.slide_set = event.presentation.slide_set
        slide.offset = 0
        slide.image = image
        slide.save()

        slides_test.append(slide)

        i += 1
        image = image_format % i

    # update the timing if a timing csv was uploaded
    if timing_value:
      timing_path = self.upload_file(timing_value, upload_to = base_path)
      offsets = utils.csv_to_offsets(timing_path)
      slides = event.presentation.slide_set.slide_set.order_by('id')
      cur_slide = 0
      for offset in offsets:
        if cur_slide < len(slides):
          slides[cur_slide].offset = offset
          slides[cur_slide].save()
          cur_slide += 1

    return True

class PresentationFormController(FormController):
  def __init__(self, request, event, instance = None, initial = {}):
    self.event = event
    FormController.__init__(self, request, PresentationForm, instance, initial = initial)

  def set_action(self, action, presenter = None):
    if action == 'add':
      label = "Add a Presenter"
    elif action == 'edit':
      label = presenter.name
    else:
      label = self.form.Meta.fieldsets[0][0]

    self.set_fieldset_label(label)

  def save(self):
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

    presentation = self.event.presentation
    if not presentation:
      presentation = Presentation()
      presentation.save()
      self.event.presentation = presentation
      self.event.save()

    presentation.presenters.add(presenter)
    presentation.save()

    return True

class SlideFormController(FormController):
  def __init__(self, request, event, instance = None):
    self.event = event
    if self.event.presentation.video:
      initial = {'video': self.event.presentation.video.id}
    else:
      initial = {}

    # make sure we grab the proper poll object, if it is one
    if instance != None:
      instance = instance.as_leaf_class()
      if type(instance) == Poll:
        initial['slide_type'] = 'poll'
        initial['poll_choices'] = '\n'.join([choice.choice for choice in instance.choice_set.all()])
        initial['poll_question'] = instance.question

    FormController.__init__(self, request, SlideForm, instance, initial = initial)

  def set_action(self, action):
    if action == 'add':
      label = 'Add a Slide'
    elif action == 'edit':
      label = 'Edit Slide'
    else:
      label = self.form.Meta.fieldsets[1][0]

    self.set_fieldset_label(label, 1)

  def reset_pdf_cache(self):
    self.event.presentation_pdf = ''
    self.event.save()

  def delete(self):
    self.reset_pdf_cache()

    FormController.delete(self)

  def save(self):
    if not self.form.is_valid():
      return False
    
    self.reset_pdf_cache()

    data = self.form.cleaned_data
    slide_set = self.event.presentation.slide_set

    if slide_set == None:
      slide_set = SlideSet()
      slide_set.presentation = self.event.presentation
      slide_set.save()
      self.event.presentation.slide_set = slide_set

    slide = self.form.instance
    if data['slide_type'] == 'poll':
      # delete the old slide if it has been changed to a poll
      if slide.id != None:
        slide.delete()

      slide = Poll()
      slide.question = data['poll_question']

    slide.slide_set = slide_set
    slide.offset = data['offset']
    if data['image']:
      base_path = os.path.dirname(slide_upload_to(slide, data['image'].name))
      slide.image = self.upload_file(data['image'], upload_to = base_path)

    self.event.presentation.video = data['video']
    slide.save()
    self.event.presentation.save()

    # we need to save the poll choices here, after the poll is saved and has an id
    if data['slide_type'] == 'poll':
      for choice_text in data['poll_choices'].split('\n'):
        print '!!!! choice: %s' % choice_text
        choice = Choice()
        choice.choice = choice_text
        choice.poll = slide
        choice.save()

    return True
