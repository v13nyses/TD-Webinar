from events.models import Event
from django.contrib import admin
#from presentations.models.admin import PresentationInline

class EventAdmin(admin.ModelAdmin):
  fieldsets = [
    ('Event Information', {'fields': ['name']}),
    ('Presentation Information', {'classes': ['collapse']}),
  ]
  #inlines = ['presentations.admin.PresentationInline']

#admin.site.register(PresentationInline)
admin.site.register(Event)
