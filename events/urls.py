from django.conf.urls.defaults import *

urlpatterns = patterns('',
  (r'^(?P<event_id>\d+)/$', 'events.views.display'),
  (r'^$', 'events.views.display'),
)
