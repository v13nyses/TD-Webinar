from django.conf.urls.defaults import *

urlpatterns = patterns('',
  url(r'event/(?P<event_id>\d+)/presentation/$', 'events.views.presentation', name = "presentation"),
  url(r'event/(?P<event_id>\d+)/presentation/(?P<state>[a-z]+)/$', 'events.views.presentation', name = "presentation_state"),
  url(r'^event/(?P<event_id>\d+)/slides/$', 'presentations.views.displaySlideSet', name = "display_slide_set"),
  url(r'^event/(?P<event_id>\d+)/state/(?P<state>[a-z]+)/$', 'events.views.event', name = "event_state"),
  url(r'^event/[\d+]/slide/(?P<slide_id>\d+)/$', 'presentations.views.displaySlide', name = "display_slide"),
#  url(r'^event/(?P<event_id>\d+)/register/$', 'registration.views.register', name = "register"),
  url(r'^event/(?P<event_id>\d+)/$', 'events.views.event', name = "event"),
  url(r'^event/(?P<event_id>\d+)/register$', 'events.views.register', name = "register"),
  url(r'^$', 'events.views.event', name = "newest_event"),
)
