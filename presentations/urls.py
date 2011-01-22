from django.conf.urls.defaults import *

urlpatterns = patterns('',
  (r'^(?P<slide_id>\d+)/$', 'presentations.views.displaySlide'),
)
