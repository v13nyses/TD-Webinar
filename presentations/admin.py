from django.contrib import admin

from presentations.models import Presentation, Presenter, PresenterType, Slide, QueuePoint, Video
from presentations.forms import SlideForm


class SlideAdmin(admin.ModelAdmin):
  form = SlideForm

  fieldsets = [
    (None, {'fields': ['presentation']}),
    ("Image Source (choose only one)", {'fields': [('image', 'pdf_file')]}),
  ]

#class PresentationInline(admin.InlineModelAdmin):
#  model = Presentation
#  extra = 1

#admin.site.register(PresentationInline)
admin.site.register(Presentation)
admin.site.register(Presenter)
admin.site.register(PresenterType)
admin.site.register(Slide, SlideAdmin)
admin.site.register(QueuePoint)
admin.site.register(Video)
