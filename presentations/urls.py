from django.conf.urls.defaults import *

urlpatterns = patterns('',
  (r'^slides/(?P<slide_id>\d+)/$', 'presentations.views.displaySlide'),
  (r'^(\d+)/queue-points/$', 'presentations.views.queuePoints'),
  
)
