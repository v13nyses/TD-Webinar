from django.conf.urls.defaults import *

urlpatterns = patterns('',
  url(r'^video-player/(?P<video_id>\w+)/(?P<player_id>\w+)/$', 'presentations.views.video_player', name = "video_player"),
)
