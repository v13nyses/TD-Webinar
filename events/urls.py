from django.conf.urls.defaults import *

urlpatterns = patterns('',
  (r'^(?P<event_id>\d+)/slides/$', 'presentations.views.displaySlideSet'),
  (r'^(?P<event_id>\d+)/slide/(?P<slide_id>)/$', 'presentations.views.displaySlide'),

  (r'^(?P<event_id>\d+)/$', 'events.views.event'),
  (r'^$', 'events.views.event'),
)
