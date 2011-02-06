from django.conf.urls.defaults import *
from forms import EventForm

urlpatterns = patterns('',
  url(r'^event/add/$', 'dashboard.views.event', name = "db_event_add"),
  url(r'^event/(?P<event_id>\d+)/$', 'dashboard.views.event', name = "db_event_edit"),

  url(r'^event/(?P<event_id>\d+)/slides/add/$', 'dashboard.views.slide', name = "db_slide_add"),
  url(r'^event/(?P<event_id>\d+)/slide/(?P<slide_id>\d+)/$', 'dashboard.views.slide', name = 'db_slide_edit'),
  url(r'^event/(?P<event_id>\d+)/slide/(?P<slide_id>\d+)/(?P<action>[a-z]+)$', 'dashboard.views.slide', name = 'db_slide_action'),

  url(r'^event/(?P<event_id>\d+)/presenters/add/$', 'dashboard.views.presenter', name = 'db_presenter_add'),
  url(r'^event/(?P<event_id>\d+)/presenter/(?P<presenter_id>\d+)/$', 'dashboard.views.presenter', name = 'db_presenter_edit'),
  url(r'^event/(?P<event_id>\d+)/presenter/(?P<presenter_id>\d+)/(?P<action>[a-z]+)+/$', 'dashboard.views.presenter', name = 'db_presenter_action'),

  url(r'^event/(?P<event_id>\d+)/preview/pre/$', 'dashboard.views.pre'),
  url(r'^event/(?P<event_id>\d+)/preview/lobby/$', 'dashboard.views.lobby'),
  url(r'^event/(?P<event_id>\d+)/preview/live/$', 'dashboard.views.live'),
  url(r'^event/(?P<event_id>\d+)/preview/post/$', 'dashboard.views.post'),
  url(r'^event/(?P<event_id>\d+)/preview/archive/$', 'dashboard.views.archive'),
  url(r'^event/(?P<event_id>\d+)/preview/email/$', 'dashboard.views.email'),
  url(r'^event/(?P<event_id>\d+)/preview/$', 'dashboard.views.pre'),
  
  url(r'^$', 'dashboard.views.event', name = 'db_event'),
)
