from django.conf.urls.defaults import *
from django.contrib import admin

urlpatterns = patterns('',
  (r'^slides/(?P<slide_id>\d+)/$', 'presentations.views.displaySlide'),
  (r'^(\d+)/queue-points/$', 'presentations.views.queuePoints'),

  (r'^presenter_type/$', 'presentations.admin_views.presenter_type_view'),
  (r'^$', admin.site.root),
  #(r'^/$',   
)
