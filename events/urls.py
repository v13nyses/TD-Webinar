from django.conf.urls.defaults import *

urlpatterns = patterns('',
  url(r'event/(?P<event_id>\d+)/presentation/$', 'events.views.presentation', name = "presentation"),
  url(r'event/(?P<event_id>\d+)/presentation/(?P<state>[a-z]+)/$', 'events.views.presentation', name = "presentation_state"),
  url(r'^event/(?P<event_id>\d+)/slides/$', 'presentations.views.displaySlideSet', name = "display_slide_set"),
  url(r'^event/(?P<event_id>\d+)/state/(?P<state>[a-z]+)/$', 'events.views.event', name = "event_state"),
  url(r'^event/[\d+]/slide/(?P<slide_id>\d+)/$', 'presentations.views.displaySlide', name = "display_slide"),
  url(r'^event/slide/(?P<poll_id>\d+)/vote$', 'polls.views.vote', name = "vote_poll"),
#  url(r'^event/(?P<event_id>\d+)/register/$', 'registration.views.register', name = "register"),
  url(r'^event/(?P<event_id>\d+)/$', 'events.views.event', name = "event"),
  url(r'^event/(?P<event_id>\d+)/register/(?P<message>.*)$', 'events.views.register', name = "register"),
  url(r'^event/(?P<event_id>\d+)/pdf$', 'events.views.pdf', name = "pdf"),
  url(r'^event/(?P<event_id>\d+)/submit_question$', 'events.views.submit_question', name = "submit_question"),
  url(r'^event/(?P<event_id>\d+)/exit_survey$', 'exitsurvey.views.exit_survey', name = "exit_survey"),
  url(r'^event/(?P<event_id>\d+)/thank_you$', 'exitsurvey.views.thank_you', name = "thank_you"),
  url(r'^event/browser-check$', 'events.views.browser_check', name = "browser_check"),
  url(r'^$', 'events.views.event', name = "newest_event"),
)
