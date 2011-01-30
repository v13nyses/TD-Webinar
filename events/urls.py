from django.conf.urls.defaults import *

urlpatterns = patterns('',
  (r'^event/(?P<event_id>\d+)/slides/$', 'presentations.views.displaySlideSet'),
  (r'^event/(?P<event_id>\d+)/slide/(?P<slide_id>)/$', 'presentations.views.displaySlide'),

  (r'^event/(?P<event_id>\d+)/register/$', 'registration.views.register'),

  (r'^event/(?P<event_id>\d+)/$', 'events.views.event'),
  (r'^$', 'events.views.event'),
)
