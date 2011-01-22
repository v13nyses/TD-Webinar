from django.conf.urls.defaults import *

urlpatterns = patterns('',
  (r'^slide/(?P<slide_id>\d+)/$', 'presentations.views.displaySlide'),
  (r'^(\d+)/queue-points/$', 'presentations.views.queuePoints'),
)
