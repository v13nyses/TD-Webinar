from django.conf.urls.defaults import *

urlpatterns = patterns('',
  url(r'^event/(?P<event_id>\d+)/slides/$', 'presentations.views.displaySlideSet', name = "display_slide_set"),
  url(r'^event/(?P<event_id>\d+)/slide/(?P<slide_id>)/$', 'presentations.views.displaySlide', name = "display_slide"),
  url(r'^event/(?P<event_id>\d+)/register/$', 'registration.views.register', name = "register"),
  url(r'^event/(?P<event_id>\d+)/$', 'events.views.event', name = "event"),
  url(r'^$', 'events.views.event', name = "newest_event"),
)
