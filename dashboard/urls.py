from django.conf.urls.defaults import *
from forms import EventForm

urlpatterns = patterns('',
  (r'^event/add/$', 'dashboard.views.event'),
  (r'^event/(?P<event_id>\d+)/$', 'dashboard.views.event'),

  (r'^event/(?P<event_id>\d+)/slides/add/$', 'dashboard.views.slides'),
  (r'^event/(?P<event_id>\d+)/slide/(?P<slide_id>\d+)/$', 'dashboard.views.slide'),

  (r'^event/(?P<event_id>\d+)/presenters/add/$', 'dashboard.views.presenters'),
  (r'^event/(?P<event_id>\d+)/presenter/(?P<presenter_id>\d+)/$', 'dashboard.views.presenter'),
  (r'^event/(?P<event_id>\d+)/presenter/(?P<presenter_id>\d+)/(?P<action>[a-z]+)+/$', 'dashboard.views.presenter'),

  (r'^event/(?P<event_id>\d+)/preview/pre/$', 'dashboard.views.pre'),
  (r'^event/(?P<event_id>\d+)/preview/lobby/$', 'dashboard.views.lobby'),
  (r'^event/(?P<event_id>\d+)/preview/live/$', 'dashboard.views.live'),
  (r'^event/(?P<event_id>\d+)/preview/post/$', 'dashboard.views.post'),
  (r'^event/(?P<event_id>\d+)/preview/archive/$', 'dashboard.views.archive'),
  (r'^event/(?P<event_id>\d+)/preview/email/$', 'dashboard.views.email'),
  (r'^event/(?P<event_id>\d+)/preview/$', 'dashboard.views.pre'),
  
  (r'^$', 'events.views.event'),
)
